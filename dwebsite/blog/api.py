from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password,make_password
from blog.models import Article,Userinfo
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import base64
import requests
import datetime

hostUrl = 'http://127.0.0.1:9000/'

#登录
@api_view(['POST'])
def dweb_login(request):
  username = request.POST['username']
  password = request.POST['password']
  #登录逻辑
  user = User.objects.filter(username=username)
  if user:
    checkPwd = check_password(password,user[0].password)
    if checkPwd:
      userinfo = Userinfo.objects.get(belong=user[0])
      token = Token.objects.get_or_create(user=user[0])
      token = Token.objects.get(user=user[0])
    else:
      return Response('pwderr')
  else:
    return Response('none')
  userinfo_data = {
    'token':token.key,
    'nickName':userinfo.nickName,
    'headImg':userinfo.headImg
  }
  return Response(userinfo_data)

#注册
@api_view(['POST'])
def dweb_register(request):
  username = request.POST['username']
  password = request.POST['password']
  password2 = request.POST['password2']
  #注册逻辑
  user = Userinfo.objects.filter(username=username)
  if user:
    return Response('repeat')
  else:
    new_password = make_password(password,username)
    newUser = User(username=username,password=new_password) 
    newUser.save()

  token = Token.objects.get_or_create(user=newUser)
  token = Token.objects.get(user=newUser)
  userinfo = Userinfo.objects.get_or_create(belong=newUser)
  userinfo = Userinfo.objects.get(belong=newUser)
  userinfo_data = {
    'token':token.key,
    'nickName':userinfo.nickName,
    'headImg':userinfo.headImg
  }
  return Response(userinfo_data)




@api_view(['POST'])
def add_article(request):
  title = request.POST['title']
  describe = request.POST['describe']
  cover = request.POST['cover']
  content = request.POST['content']
  
  #保存文章
  new_article = Article(title=title)
  new_article.save()
  #解析富文本html文档
  soup = BeautifulSoup(content, 'html.parser')
  #获取所有img标签 图片
  imgList = soup.find_all('img')
  # print(imgList)
  for img in range(0,len(imgList)):
    src = imgList[img]['src']
    # 判断图片 是远程 还是 本地
    if 'http://' in src or 'https://' in src:
      # print('远程图片')
      # 请求远程图片
      image = requests.get(src)
      #转化二进制
      image_data = Image.open(BytesIO(image.content))
      print(image_data)
      # 设定文件名称
      image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id)+'-'+str(img)
      image_data.save("upload/"+ image_name +".png")
      new_src = hostUrl + "upload/"+ image_name +".png"
      content = content.replace(src,new_src)
      # 封面设定
      if cover == src:
        cover = new_src
    else:
      # print('本地图片')
      image_data = base64.b64decode(src.split(',')[1])
      image_name =datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id)+'-' +str(img)+'.' + src.split(',')[0].split('/')[1].split(';')[0]
      # print(image_name)
      image_url = os.path.join('upload',image_name).replace('\\','/')
      with open(image_url,'wb') as f:
        f.write(image_data)
      # print(image_url)
      new_src = hostUrl + image_url
      content = content.replace(src,new_src)
      # 封面设定
      if cover == src:
        cover = new_src
      
  
  new_article.content = content
  new_article.describe = describe
  new_article.cover = cover
  new_article.save()
  return Response('ok')