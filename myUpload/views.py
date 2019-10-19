from django.shortcuts import render
from django.http import HttpResponse
from myUpload.models import BookResources,BookPinglun,BookCollection,BookReport
from shuchongwo.models import bookT
import time
# Create your views here.
def book_resources(request):
    if request.method == "POST":
        type = request.POST['type']
        if type=='' or type==None:
            return HttpResponse('error')
        elif type=='text':
            bid = request.POST['bid']
            uid = request.session.get("uid",None)
            link = request.POST['link']
            if uid == None:
                uid = 0
            if bid !='' and link !='':
                try:
                    res = BookResources()
                    res.bid = bid
                    res.uid = uid
                    res.type = 'txt'
                    res.link = link
                    res.save()
                    return HttpResponse('suc')
                except :
                    return HttpResponse('error')
            else:
                return HttpResponse('error')
        elif type == 'file':
            File =request.FILES.get("res", None)    # 获取上传的文件，如果没有文件，则默认为None 
            if not File:
                return HttpResponse("error")
            bid = request.POST['bid']
            uid = request.session.get("uid",None)
            if uid == None:
                uid = 0
            if bid:
                res = open("shuchongwo/static/shuchongwo/book/"+str(bid)+"/" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + File.name,'wb+')    # 打开特定的文件进行二进制的写操作 
                for chunk in File.chunks():      # 分块写入文件 
                    res.write(chunk) 
                res.close()
                try:
                    res = BookResources()
                    res.bid = bid
                    res.uid = uid
                    res.type = 'file'
                    res.link = "/static/shuchongwo/book/"+str(bid)+"/" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + File.name
                    res.save()
                    return HttpResponse('suc')
                except :
                    return HttpResponse('error')

            return HttpResponse('error')
        else:
            return HttpResponse('error')

    return HttpResponse('error')

def book_pinglun(request):
    if request.method == "POST":
        bid = request.POST['bid']
        uid = request.session.get("uid",None)
        if uid == None:
            uid = 0
        pinglun = request.POST['pinglun']

        if bid and pinglun:
            try:
                p = BookPinglun()
                p.bid = bid
                p.uid = uid
                p.pinglun = pinglun
                p.save()
                return HttpResponse('suc')
            except :
                return HttpResponse('error')
        
    return HttpResponse('error')

def book_r(request):
    if request.method == 'GET':
        bid = request.GET['bid']
        r = request.GET['r']
        if r == 'recommend':
            try:
                bt = bookT.objects.get(bid = bid)
                bt.recommend = bt.recommend + 1
                bt.save()
                return HttpResponse('suc')
            except :
                print('recommend_error')
                return HttpResponse('error')
        elif r == 'collection':
            uid = request.session.get("uid",None)
            if uid == None:
                return HttpResponse('unlogin')
            check = BookCollection.objects.filter(bid = bid,uid=uid)
            if len(check) > 0 :
                return HttpResponse('repeat')
            try:
                bt = bookT.objects.get(bid = bid)
                bt.collection = bt.collection + 1
                bt.save()

                bc  = BookCollection()
                bc.bid = bid
                bc.uid = uid
                bc.save()
                return HttpResponse('suc')
            except :
                print('collection_error')
                return HttpResponse('error')
            return HttpResponse('error')
        elif r == 'report':
            uid = request.session.get("uid",None)
            if uid == None:
                uid = 0
            try:
                br = BookReport()
                br.bid = bid
                br.uid = uid
                br.save()
                return HttpResponse('suc')
            except :
                print('report_error')
                return HttpResponse('error')
        else:
            return HttpResponse('error')
    return HttpResponse('error')

def delc(request):
    if request.method == "GET":
        try:
            bid = request.GET['bid']
            c = request.GET['c']
            uid = request.session.get('uid',None)
            if uid == None:
                return HttpResponse('nologin')
            if c == 'collection':
                BookCollection.objects.filter(uid=uid,bid=bid).delete()
                bt = bookT.objects.get(bid = bid)
                bt.collection = bt.collection - 1
                bt.save()
            return HttpResponse('suc') 
        except:
            HttpResponse('error')
        
    return HttpResponse('error')

def delr(request):
    if request.method == "GET":
        try:
            rid = request.GET['rid']
            uid = request.session.get('uid',None)
            if uid == None:
                return HttpResponse('nologin')

            BookResources.objects.filter(uid=uid,id=rid).delete()
            return HttpResponse('suc') 
        except:
            HttpResponse('error')
        
    return HttpResponse('error')