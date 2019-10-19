from django.shortcuts import render
from django.http import HttpResponse
from shuchongwo.models import bookf,btable,bookT
import json
# Create your views here.
def createTop(request):
    name = request.session.get('uname',None)
    if name!='admin':
        return HttpResponse('不是管理员不能使用该页面')
    bf = bookf.objects.filter()
    for b in bf:
        bt = bookT()
        bt.bid = b.id
        bt.click = 0
        bt.collection = 0
        bt.recommend = 0
        bt.save()

    return HttpResponse('session')
def updatabooks(request):
    name = request.session.get('uname',None)
    if name!='admin':
        return HttpResponse('不是管理员不能使用该页面')
    if request.method == "POST":
        uf = request.FILES.get('ufile',None)
        if not uf:
            return HttpResponse('文件上传出错')
        w = open('upload/'+ uf.name,'wb+')
        for chunk in uf.chunks():      # 分块写入文件 
            w.write(chunk) 
        w.close() 
        r = open('upload/'+ uf.name,'r',encoding='utf-8')
        for b in r.readlines():
            book = json.loads(b)
            bf = bookf()
            bf.bname = book['name']
            bf.author = book['author']
            bf.words = float(book['words'][0:-2])
            bf.bclass = book['bclass']
            bf.newz = book['newz']
            bf.description = book['description']
            bf.burl = book['burl']
            bf.save()
            if book['table'] != '':
                for item in book['table']:
                    bt = btable()
                    bt.bid = bf.id
                    bt.table = item
                    bt.save()
        
        return HttpResponse('sessfu')

    else :
        return render(request,'updatebook.html')

def getjson(request):
    bf = bookf.objects.filter()
    w = open('D:/b.json','w+',encoding='utf-8')
    for b in bf:
        book = {}
        book['id'] = b.id
        book['url'] = b.burl.split('/')[4]
        w.write(json.dumps(book,ensure_ascii=False) + '\n')
    return HttpResponse('成功')

