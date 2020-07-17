from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# #用户信息
# class Userinfo(models.Model):
#     headImg = models.ImageField()
#     nickName = models.CharField()
#     belong = models.OneToOneField(User)
#     def __int__(self):
#         return self.id


# #文章分类
# class Category(models.Model):
#     name = models.CharField()
#     belong = models.ForeignKey(self)
#     def __int__(self):
#         return self.id

#文章
class Article(models.Model):
    title = models.CharField(null=True,blank=True,max_length=80)
    cover = models.CharField(null=True,blank=True,max_length=300)
    describe = models.CharField(null=True,blank=True,max_length=200)
    content = models.TextField()
    # belong = models.ForeignKey(Userinfo)
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
