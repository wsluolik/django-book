from django.shortcuts import render
# Create your views here.
from shuchongwo.models import Users,recommend,bookf,bookT,rec_table,btable
from shuchongwo.forms import regForm,loginForm
from myUpload.models import BookResources,BookPinglun,BookCollection
from django.http import HttpResponse
from django.db.models import Q
import json
def index(request):
    dic = {}
    rec = recommend.objects.order_by('-id')[:6]
    rec_list = []
    for r in rec:
        rec_item={}
        rec_item['bid'] = r.bid
        rbf = bookf.objects.get(id = r.bid)
        rec_item['bname'] = rbf.bname
        rec_item['author'] = rbf.author
        rec_item['description'] = rbf.description
        rec_list.append(rec_item)
    dic['rec_list'] = rec_list

    rec = rec_table.objects.order_by('-id')[:10]
    rec_table_list = []
    for r in rec:
        rec_table_list.append(r.tablename)
    dic['rec_table_list'] = rec_table_list

    top_click = bookT.objects.order_by('-click')[:10]
    top_click_list = []
    for i in top_click:
        t_item={}
        t_item['bid'] = i.bid
        tbf = bookf.objects.get(id = i.bid)
        t_item['bname'] = tbf.bname
        t_item['author'] = tbf.author
        t_item['newz'] = tbf.newz
        top_click_list.append(t_item)
    dic['top_click_list'] = top_click_list

    top_collection = bookT.objects.order_by('-collection')[:10]
    top_collection_list = []
    for i in top_collection:
        t_item={}
        t_item['bid'] = i.bid
        tbf = bookf.objects.get(id = i.bid)
        t_item['bname'] = tbf.bname
        t_item['author'] = tbf.author
        t_item['newz'] = tbf.newz
        top_collection_list.append(t_item)
    dic['top_collection_list'] = top_collection_list

    top_recommend = bookT.objects.order_by('-recommend')[:10]
    top_recommend_list = []
    for i in top_recommend:
        t_item={}
        t_item['bid'] = i.bid
        tbf = bookf.objects.get(id = i.bid)
        t_item['bname'] = tbf.bname
        t_item['author'] = tbf.author
        t_item['newz'] = tbf.newz
        top_recommend_list.append(t_item)
    dic['top_recommend_list'] = top_recommend_list


    return render(request,'index.html',dic)
def login(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            remember = form.cleaned_data['remember']
            checknumber = form.cleaned_data['checknumber']
            # print('name:' + name + '  password:' +password + '   remember' + str(remember) + '  checknumber' +  checknumber )
            e = {}
            if checknumber != request.session.get('check_number',None):
                e = {'error':'验证码错误'} 
                return render(request,'login.html',e)
            try:
                u = Users.objects.get(username=name)
                if u.password == password:
                    try:
                        del request.session['check_number']
                    except:
                        pass
                    request.session['uid'] = u.id
                    request.session['uname'] = u.username
                    if remember:
                        pass
                    else:
                        request.session.set_expiry(43200)
                    referer = referer = request.session.get('referer',None)
                    try:
                        del request.session['referer']
                    except:
                        pass
                    return render(request,'jump.html',{'info':'登录成功','url':referer})
                    
                else:
                    e = {'error':'密码错误'}
                    return render(request,'login.html',e)
            except:
                e = {'error':'用户名不存在'}
                return render(request,'login.html',e)
        else:
            return HttpResponse(str(form.errors))
    else:
        referer =request.META['HTTP_REFERER']
        if referer !='':
            request.session['referer'] = referer
        else:
            request.session['referer'] = '/index'
        return render(request,'login.html')
def registered(request):
    if request.method == 'POST':# 当提交表单时
        
        form = regForm(request.POST) # form 包含提交的数据  
        if form.is_valid():# 如果提交的数据合法
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            sex = form.cleaned_data['sex']
            checknumber = form.cleaned_data['checknumber']
            # print('name:'+name)
            # print('email:'+email)
            # print('password:'+password)
            # print('sex:'+sex)
            # print('checknumber:'+checknumber)
            if checknumber != request.session.get("check_number",None):
                return HttpResponse("验证码错误！")
            try:
                del request.session['check_number']
            except:
                pass
            user = Users()
            user.username = name
            user.password = password
            user.email = email
            if sex == '0':
                user.sex = False
            else:
                user.sex = True
            try:
                user.save()
                u = Users.objects.get(username=name)
                request.session['uid'] = u.id
                request.session['uname'] = u.username
                referer = referer = request.session.get('referer',None)
                try:
                    del request.session['referer']
                except:
                    pass
                return render(request,'jump.html',{'info':'注册成功','url':referer})
            except:
                return HttpResponse("未知错误，注册失败")
            
        else:
            return HttpResponse(str(form.errors))
     
    else:# 当正常访问时
        referer =request.META['HTTP_REFERER']
        if referer !='':
            request.session['referer'] = referer
        else:
            request.session['referer'] = '/index'
        return render(request,'registered.html')   
def Logout(request):
    try:
        del request.session['uid']
        del request.session['uname']
        return render(request,'jump.html',{'info':'注销成功','url':'/index'})
    except :
        return HttpResponse('注销失败，请确认登录状态')
def Search(request):
    n = ''
    try:
        n = request.GET['n']
        if n == '':
            return HttpResponse('搜索条件为空')
    except :
        return HttpResponse('搜索条件为空')
    dic = {}
    try:     
        results = bookf.objects.filter(Q(bname__contains=n)|Q(author__contains=n))
        s_list = []
        for r in results:
            c_item={}
            
            c_item['bid'] = r.id
            c_item['bname'] = r.bname
            c_item['author'] = r.author
            c_item['newz'] = r.newz
            c_item['description'] = r.description
            s_list.append(c_item)
        dic['search_list'] = s_list

        top_recommend = bookT.objects.order_by('-recommend')[:6]
        top_recommend_list = []
        for i in top_recommend:
            t_item={}
            t_item['bid'] = i.bid
            tbf = bookf.objects.get(id = i.bid)
            t_item['bname'] = tbf.bname
            t_item['author'] = tbf.author
            t_item['newz'] = tbf.newz
            top_recommend_list.append(t_item)
        dic['recommend'] = top_recommend_list
    except:
        return HttpResponse('未知错误！')
    return render(request,'search.html',dic)
def User(request,r_uid):
    if r_uid == 0:
        return HttpResponse('用户不存在')
    try:
        dic = {}
        u_c = BookCollection.objects.filter(uid = r_uid)
        c_list = []
        for r in u_c:
            c_item={}
            c_item['bid'] = r.bid
            rbf = bookf.objects.get(id = r.bid)
            c_item['bname'] = rbf.bname
            c_item['author'] = rbf.author
            c_item['newz'] = rbf.newz
            c_item['description'] = rbf.description
            c_list.append(c_item)
        dic['collection_list'] = c_list

        res = []
        b_res = BookResources.objects.filter(uid = r_uid)
        if len(b_res)!=0:
            for r in b_res:
                item = {}
                item['id'] = r.id
                item['type'] = r.type
                item['link'] = r.link
                item['date'] = r.create_time
                if item['type'] == 'file':
                    item['filename'] = r.link.split('/')[-1]
                if r.uid!=0:
                    u = Users.objects.get(id=r.uid)
                    item['updata_name'] = u.username
                else:
                    item['updata_name'] = '佚名'
                item['updata_uid'] = r.uid
                res.append(item)
            dic['res'] = res
        else:
            dic['res'] = ''

        top_recommend = bookT.objects.order_by('-recommend')[:6]
        top_recommend_list = []
        for i in top_recommend:
            t_item={}
            t_item['bid'] = i.bid
            tbf = bookf.objects.get(id = i.bid)
            t_item['bname'] = tbf.bname
            t_item['author'] = tbf.author
            t_item['newz'] = tbf.newz
            top_recommend_list.append(t_item)
        dic['recommend'] = top_recommend_list
    except:
        return HttpResponse('未知错误！')
    return render(request,'user.html',dic)

def Book(request,bid):
    dic = {}
    book = {}
    bf = bookf.objects.get(id = bid)
    if bf !=None:
        book['bid'] = bid
        book['name'] = bf.bname
        book['author'] = bf.author
        book['words'] = bf.words
        book['bclass'] = bf.bclass
        book['newz'] = bf.newz
        book['descirption'] = bf.description
        book['burl'] = bf.burl
        dic['book'] = book
    else:
        return HttpResponse("出现错误，书籍不存在")
    try:
        bt = bookT.objects.get(bid = bid)
        bt.click = bt.click + 1
        bt.save()
    except:
        print('bterror')
    try:
        label = []
        b_lable = btable.objects.filter(bid = bid)
        for b in b_lable:
            label.append(b.table)
        dic['lable'] = label
    except :
        dic['lable'] = ''

    mulu = []
    r_mulu = open("shuchongwo/static/shuchongwo/book/"+str(bid)+"/directory.json",'r',encoding='utf-8')

    for item in r_mulu.readlines():
        li = json.loads(item)
        mulu.append(li['cn'])
    r_mulu.close()
    dic['mulu'] = mulu

    try:
        res = []
        b_res = BookResources.objects.filter(bid = bid)
        for r in b_res:
            item = {}
            item['type'] = r.type
            item['link'] = r.link
            if item['type'] == 'file':
                item['filename'] = r.link.split('/')[-1]
            if r.uid!=0:
                u = Users.objects.get(id=r.uid)
                item['updata_name'] = u.username
            else:
                item['updata_name'] = '佚名'
            item['updata_uid'] = r.uid
            res.append(item)
        dic['res'] = res
    except :
        dic['res'] = ''

    try:
        pl = []
        pls = BookPinglun.objects.filter(bid = bid)
        for p in pls:
            item = {}
            item['uid'] = p.uid
            item['pl'] = p.pinglun
            if p.uid!=0:
                u = Users.objects.get(id=p.uid)
                item['uname'] = u.username
            else:
                item['uname'] = '游客'
            pl.append(item)
        if len(pl) == 0:
            dic['pinglun'] = ''
        else:
            dic['pinglun'] = pl
    except :
        dic['pinglun'] = ''

    return render(request,'book.html',dic)

def RankList(request):
    dic = {}
    
    type_ = ''
    page = 1
    pages = 1
    try:
        type_ = request.GET['type']
    except :
        type_ = 'hot'
    try:
        page = int(request.GET['page'])
    except :
        page = 1
    
    count = bookT.objects.count()
    pages = int(count / 10)
    if (count % 10) != 0:
        pages = pages + 1
    if page < 1 and page > pages:
        return HttpResponse('页码不正确')
    start_num = 0
    end_num = 0
    if page < pages:
        end_num = page * 10
        start_num = end_num - 10
    elif page == pages:
        start_num = page * 10 - 10
        end_num = count
    BT = object
    print(type_)
    print(type(type_))
    if type_ == 'hot':
        BT = bookT.objects.order_by('-click')[start_num:end_num]
    elif type_ ==  'recommend':
        BT = bookT.objects.order_by('-recommend')[start_num:end_num]
    elif type_ ==  'collection':
        BT = bookT.objects.order_by('-collection')[start_num:end_num]
    else:
        return HttpResponse('type error')
    bt_list = []
    for i in BT:
        t_item={}
        t_item['bid'] = i.bid
        tbf = bookf.objects.get(id = i.bid)
        t_item['bname'] = tbf.bname
        t_item['author'] = tbf.author
        t_item['newz'] = tbf.newz
        t_item['description'] = tbf.description
        bt_list.append(t_item)
    dic['bt_list'] = bt_list
    

    dic['page'] = page
    dic['pages'] = pages
    if page > 1:
        dic['previous'] = page - 1
    else :
        dic['previous'] = 1
    if page < pages:
        dic['next'] = page + 1
    else :
        dic['next'] = pages
    dic['tp'] = type_
    try:
        top_recommend = bookT.objects.order_by('-recommend')[:6]
        top_recommend_list = []
        for i in top_recommend:
            t_item={}
            t_item['bid'] = i.bid
            tbf = bookf.objects.get(id = i.bid)
            t_item['bname'] = tbf.bname
            t_item['author'] = tbf.author
            t_item['newz'] = tbf.newz
            top_recommend_list.append(t_item)
        dic['recommend'] = top_recommend_list
    except:
        return HttpResponse('未知错误！')
    return render(request,'ranklist.html',dic)