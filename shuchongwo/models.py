from django.db import models

# Create your models here.
#用户表
class Users(models.Model):
    username = models.CharField(max_length=12,unique=True,null=False)
    password = models.CharField(max_length=30,null=False)
    email = models.CharField(max_length=80)
    sex = models.BooleanField(default=0)
    create_time = models.DateField(auto_now_add=True)
    class Meta:
        db_table="Users"
    def __str__(self):
        return self.username
#书基本信息
class bookf(models.Model):
    id = models.AutoField(primary_key=True)
    bname = models.CharField(max_length=30,null=False)
    author = models.CharField(max_length=30)
    words = models.FloatField()
    bclass = models.CharField(max_length=30)
    newz= models.CharField(max_length=80)
    description = models.CharField(max_length=500)
    burl = models.CharField(max_length=200)
    class Meta:
        db_table="bookf"
    def __str__(self):
        return self.bname
#书拥有的标签
class btable(models.Model):
    bid = models.IntegerField(null=False)
    table = models.CharField(max_length=20,null=False)
    class Meta:
        db_table="btable"
#书的点击，推荐，收藏
class bookT(models.Model):
    bid = models.IntegerField(primary_key=True)
    click = models.IntegerField(null=False)
    collection = models.IntegerField(null=False)
    recommend = models.IntegerField(null=False)
#管理员推荐的书
class recommend(models.Model):
    bid = models.IntegerField(null=False)

#管理员推荐的标签
class rec_table(models.Model):
    tablename = models.CharField(max_length=20,null=False)
    

    

