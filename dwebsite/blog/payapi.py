from alipay.aop.api.AlipayClientConfig import AlipayClientConfig  # 客户端配置类
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient  # 默认客户端类
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel  # 网站支付数据模型类
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest  # 网站支付请求类
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from django.shortcuts import HttpResponse
from dwebsite import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from blog.models import Article, PayOrder
import datetime
import random

@api_view(['POST'])
def getAlipayUrl(request):
  token = request.POST['token']
  
  user_token = Token.objects.filter(key=token)
  if len(user_token) == 0:
      return Response('nologin')
  user = user_token[0].user
  article_id=request.POST['article_id']
  article = Article.objects.get(id=article_id)

  nowtime = datetime.datetime.now()
  new_payorder = PayOrder(belong_user=user,belong=article)
  new_payorder.order = str(nowtime.year) + str(random.randrange(10000000,99999999))
  # print(new_payorder.order)
  new_payorder.price = '0.01'
  new_payorder.save()

  alipay_client_config = AlipayClientConfig()
  alipay_client_config.server_url = settings.ALIPAY_URL
  alipay_client_config.app_id = settings.ALIPAY_APPID
  alipay_client_config.app_private_key = settings.APP_PRIVATE_KEY
  alipay_client_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY

  client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
  model = AlipayTradePagePayModel()  # 创建网站支付模型
  model.out_trade_no = new_payorder.order
  model.total_amount = new_payorder.price
  model.subject = "打赏订单："+new_payorder.order+'/'+new_payorder.price+'元'
  model.product_code = 'FAST_INSTANT_TRADE_PAY'
  model.timeout_express = '5m'


  #发送请求
  pay_request = AlipayTradePagePayRequest(biz_model=model)
  pay_request.notify_url = settings.ALIPAY_NOTIFY_URL
  pay_request.return_url = settings.ALIPAY_RETURN_URL
  response = client.page_execute(pay_request, http_method='GET')
  # print(response)
  pay_link = response
  return Response({'pay_link':pay_link})




@api_view(['POST'])
def payResult(request):
  # print(request.POST)
  if request.method == "POST":
    params = request.POST.dict()
    order = params['out_trade_no']
    print(order)
    if checkSign(params):
      payOrder = PayOrder.objects.filter(order=order)
      if payOrder:
        payOrder[0].status = True
        payOrder[0].save()
        print('支付成功')
        return HttpResponse('success')
      else:
        print('支付失败')
        return HttpResponse('')
    else:
      print('支付失败 认证失败')
      return HttpResponse('')
    



def checkSign(params):
  sign = params.pop('sign', None)  # 取出签名
  params.pop('sign_type', None)  # 取出签名类型
  params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
  message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
  # with open(settings.ALIPAY_PUBLIC_KEY_PATH, 'rb') as public_key: # 打开公钥文件
  try:
      #     status =verify_with_rsa(public_key.read().decode(),message,sign) # 验证签名并获取结果
      status = verify_with_rsa(settings.ALIPAY_PUBLIC_KEY.encode('utf-8').decode('utf-8'), message, sign)  # 验证签名并获取结果
      return status  # 返回验证结果
  except:  # 如果验证失败，返回假值。
      return False