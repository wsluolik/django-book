from django.db import models

# Create your models here.
#书的分享资源
class BookResources(models.Model):
    bid = models.IntegerField(null=False)
    uid = models.IntegerField(null=False)
    type = models.CharField(max_length=30,null=False)
    link = models.CharField(max_length=255,null=False)
    create_time = models.DateField(auto_now_add=True)
#书的评论
class BookPinglun(models.Model):
    bid = models.IntegerField(null=False)
    uid = models.IntegerField(null=False)
    pinglun = models.CharField(max_length=512,null=False)
    create_time = models.DateField(auto_now_add=True)

#用户收藏
class BookCollection(models.Model):
    bid = models.IntegerField(null=False)
    uid = models.IntegerField(null=False)
    create_time = models.DateField(auto_now_add=True)

#举报
class BookReport(models.Model):
    bid = models.IntegerField(null=False)
    uid = models.IntegerField(null=False)
    transaction = models.BooleanField(default=False)
    create_time = models.DateField(auto_now_add=True)
