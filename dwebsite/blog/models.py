from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#用户信息
class Userinfo(models.Model):
    headImg = models.CharField(null=True,blank=True,max_length=200)
    nickName = models.CharField(null=True,blank=True,max_length=200)
    belong = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    def __int__(self):
        return self.id


#文章分类
class Lanmu(models.Model):
    name = models.CharField(null=True,blank=True,max_length=80)
    belong = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='lanmu_children')
    def __int__(self):
        return self.id

#文章
class Article(models.Model):
    title = models.CharField(null=True,blank=True,max_length=80)
    cover = models.CharField(null=True,blank=True,max_length=300)
    describe = models.CharField(null=True,blank=True,max_length=200)
    content = models.TextField()
    belong = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='article_user')
    belong_lanmu = models.ForeignKey(Lanmu,on_delete=models.CASCADE,null=True,blank=True,related_name='article_lanmu')
    def __int__(self):
        return self.id

# #收藏
# class Favourite(modesl.Model):
#     belong_user = models.ForeignKey(Userinfo)
#     belong_art = models.ForeignKey(Article)
#     def __int__(self):
#         return self.id

# #点赞
# class Like(models.Model):
#     belong_art = models.ForeignKey(Article)
#     # num = models.IntegerField()
#     belong_user = models.ForeignKey(Userinfo)
#     def __int__(self):
#         return self.id

# #打赏
# class PayOrder(models.Model):
#     order = models.CharField()
#     price = models.CharField()
#     status = models.BooleanField()
#     def __int__(self):
#         return self.id
