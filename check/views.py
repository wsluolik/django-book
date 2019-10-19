from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from io import BytesIO
from shuchongwo.models import Users
# Create your views here.
def checkNumber(request):
    img = Image.new('RGB',(100,30),(255,255,255))
    draw = ImageDraw.Draw(img)
    for i in range(200):
        draw.point((random.randint(0,100),random.randint(0,30)),(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    for i in range(10):
        draw.line(
            [
                (random.randint(0, 100), random.randint(0, 30)),
                (random.randint(0, 100), random.randint(0, 30))
            ],
            (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        )


    # params = [
    #         1 - float(random.randint(1,2)) / 100,
    #         0,
    #         0,
    #         0,
    #         1 - float(random.randint(1,10)) / 100,
    #         float(random.randint(1,2)) / 500,
    #         0.001,
    #         float(random.randint(1,2)) / 500
    #     ]
    # img = img.transform((150,50), Image.PERSPECTIVE, params)
    # img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    str_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','p','q','r','s','t','u','v','w','x','y','z',
    '1','2','3','4','5','6','7','8','9'
    ]
    draw_str = ''
    for i in range(4):
        draw_str = draw_str + str_list[random.randint(0,33)]
    # print(draw_str)
    request.session['check_number'] = draw_str
    m_font = ImageFont.truetype('C:/Windows/fonts/cambriai.ttf',24)
    draw.text((random.randint(6,40),random.randint(3,8)),draw_str,font=m_font,fill=(0,0,205))
    print('*'*50)
    # img.show()
    checkDate = BytesIO()
    img.save(checkDate,'PNG')
    return HttpResponse(checkDate.getvalue(),content_type="image/png")

def check_username(request):
    name = ''
    try:
        name = request.GET['name']
    except:
        return HttpResponse('0')
    if name == "":
        return HttpResponse('0')
    else:
        u = Users.objects.filter(username=name)
        if u.count() == 0 :
            return HttpResponse('1')
        else:
            return HttpResponse('0')
def check_num(request):
    num = request.GET['checknum']
    s_num = request.session.get("check_number")
    if s_num=="" or num == "":
        return HttpResponse('0')
    else:
        if s_num == num :
            return HttpResponse('1')
        else:
            return HttpResponse('0') 