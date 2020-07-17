from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import Article
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import datetime

hostUrl = 'http://127.0.0.1:9000/'

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
    else:
      # print('本地图片')
      pass
  
  new_article.content = content
  new_article.save()
  return Response('ok')