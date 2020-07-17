from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import Article
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import datetime
import requests

@api_view(['POST'])
def add_article(request):
  title = request.POST['title']
  describe = request.POST['describe']
  cover = request.POST['cover']
  content = request.POST['content']

  #新建文章
  new_article = Article(title=title)
  new_article.save()

  soup = BeautifulSoup(content, 'html.parser')
  #获取文章中的图片
  imgList = soup.find_all('img')
  # print(imgList)
  for img in range(0,len(imgList)):
    src = imgList[img]['src']
    
    if 'http://' or 'https://' in src:
      print(src)
      image = requests.get(src)
      print(image)
      #转换二进制
      image_data = Image.open(BytesIO(image.content))
      #保存图片
        #文件名唯一 时间 + 文章id + 图片位标
      image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id)+'-'+str(img)
      print(image_name)
      image_data.save("upload/"+image_name+'.png')
    else:
      pass
  return Response('ok')