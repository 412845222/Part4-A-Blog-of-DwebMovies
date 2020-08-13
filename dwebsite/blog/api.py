from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Article, Userinfo, Lanmu
from django.contrib.auth.models import User, Group, Permission, ContentType
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import base64
import requests
import datetime
import json

hostUrl = 'http://127.0.0.1:9000/'


# 鉴权
@api_view(['POST'])
def dweb_checkPerm(request):
    # print(request.POST)
    token = request.POST['token']
    content_type = request.POST['contentType']
    permissions = json.loads(request.POST['permissions'])

    # print(token)
    # print(content_type)
    # print(permissions[0])
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for p in permissions:
            app_str = content_type.split('_')[0]
            model_str = content_type.split('_')[1]
            perm_str = app_str + '.' + p + '_'+model_str
            print(perm_str)
            check = user.has_perm(perm_str)
            print(check)
            if check == False:
                return Response('noperm')
    else:
        return Response('nologin')

    return Response('ok')


# 登录
@api_view(['POST'])
def dweb_login(request):
    username = request.POST['username']
    password = request.POST['password']
    # 登录逻辑
    user = User.objects.filter(username=username)
    if user:
        checkPwd = check_password(password, user[0].password)
        if checkPwd:
            userinfo = Userinfo.objects.get_or_create(belong=user[0])
            userinfo = Userinfo.objects.get(belong=user[0])
            token = Token.objects.get_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
        else:
            return Response('pwderr')
    else:
        return Response('none')
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg
    }
    return Response(userinfo_data)

# 注册


@api_view(['POST'])
def dweb_register(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    # 注册逻辑
    user = User.objects.filter(username=username)
    if user:
        return Response('repeat')
    else:
        new_password = make_password(password, username)
        newUser = User(username=username, password=new_password)
        newUser.save()

    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    userinfo = Userinfo.objects.get_or_create(belong=newUser)
    userinfo = Userinfo.objects.get(belong=newUser)
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg
    }
    return Response(userinfo_data)

# 自动登录


@api_view(['POST'])
def dweb_autoLogin(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if user_token:
        userinfo = Userinfo.objects.get(belong=user_token[0].user)
        userinfo_data = {
            'token': token,
            'nickName': userinfo.nickName,
            'headImg': userinfo.headImg
        }
        return Response(userinfo_data)
    else:
        return Response('tokenTimeout')

# 登出


@api_view(['POST'])
def dweb_logout(request):
    token = request.POST['token']
    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')


# 文章发布
@api_view(['POST','PUT'])
def add_article(request):
    token = request.POST['token']
    if request.method == "PUT":
        permList = [
            'blog.change_article'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        
        lanmu_id = request.POST['lanmu_id']
        article_id = request.POST['article_id']

        lanmu = Lanmu.objects.get(id=lanmu_id)
        article = Article.objects.get(id=article_id)
        article.belong_lanmu = lanmu
        article.save()
        return Response('ok')


    title = request.POST['title']
    describe = request.POST['describe']
    cover = request.POST['cover']
    content = request.POST['content']
    

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')
    if len(title) == 0:
        return Response('notitle')

    # 保存文章
    new_article = Article(title=title)
    new_article.save()
    # 解析富文本html文档
    soup = BeautifulSoup(content, 'html.parser')
    # 获取所有img标签 图片
    imgList = soup.find_all('img')
    # print(imgList)
    for img in range(0, len(imgList)):
        src = imgList[img]['src']
        # 判断图片 是远程 还是 本地
        if 'http://' in src or 'https://' in src:
            # print('远程图片')
            # 请求远程图片
            image = requests.get(src)
            # 转化二进制
            image_data = Image.open(BytesIO(image.content))
            print(image_data)
            # 设定文件名称
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-' + \
                str(new_article.id)+'-'+str(img)
            image_data.save("upload/" + image_name + ".png")
            new_src = hostUrl + "upload/" + image_name + ".png"
            content = content.replace(src, new_src)
            # 封面设定
            if cover == src:
                cover = new_src
        else:
            # print('本地图片')
            image_data = base64.b64decode(src.split(',')[1])
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'-'+str(new_article.id) + \
                '-' + str(img)+'.' + \
                src.split(',')[0].split('/')[1].split(';')[0]
            # print(image_name)
            image_url = os.path.join('upload', image_name).replace('\\', '/')
            with open(image_url, 'wb') as f:
                f.write(image_data)
            # print(image_url)
            new_src = hostUrl + image_url
            content = content.replace(src, new_src)
            # 封面设定
            if cover == src:
                cover = new_src

    new_article.content = content
    new_article.describe = describe
    new_article.cover = cover
    new_article.belong = user_token[0].user
    new_article.save()
    return Response('ok')

# 文章分页 数据列表


@api_view(['GET'])
def articleList(request):
    page = request.GET['page']
    pageSize = request.GET['pageSize']
    lanmu = request.GET['lanmu']

    if lanmu=='all':
        articles = Article.objects.all()
    elif lanmu=='nobelong':
        articles = Article.objects.filter(belong_lanmu=None)
    else:
        articles = Article.objects.filter(belong_lanmu__name=lanmu)
    total = len(articles)
    paginator = Paginator(articles, pageSize)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # print(articles)
    articles_data = []
    for a in articles:
        a_item = {
            'title': a.title,
            'cover': a.cover,
            'nickName': '',
            'id': a.id
        }
        article_user = a.belong
        userinfo = Userinfo.objects.filter(belong=article_user)
        if userinfo[0].nickName:
            a_item['nickName'] = userinfo[0].nickName
        else:
            a_item['nickName'] = article_user.username
        # print(a_item['nickName'])
        articles_data.append(a_item)

    return Response({'data': articles_data, 'total': total})

# 删除文章


@api_view(['DELETE'])
def deleteArticle(request):
    article_id = request.POST['id']
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')

    user = user_token[0].user
    user_perm = user.has_perm("blog.delete_article")
    print("文章删除权限")
    print(user_perm)
    if user_perm == False:
        return Response('noperm')
    print(article_id)
    article = Article.objects.get(id=article_id)
    article.delete()
    return Response('ok')


# 用户列表
@api_view(['GET'])
def dweb_userlist(request):
    user_list = User.objects.all()
    user_list_data = []
    for user in user_list:
        user_item = {
            "name": user.username
        }
        user_list_data.append(user_item)
    return Response(user_list_data)


# 用户组管理
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def dweb_group(request):
    # 获取用户组列表
    if request.method == "GET":
        groups = Group.objects.all()
        groups_data = []
        for g in groups:
            g_item = {
                "name": g.name
            }
            groups_data.append(g_item)
        return Response(groups_data)
    # 用户 分配 用户组
    if request.method == "POST":
        token = request.POST['token']
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        gourp_name = request.POST['group']
        userlist_name = json.loads(request.POST['userlist'])

        group = Group.objects.get(name=gourp_name)

        for username in userlist_name:
            user = User.objects.get(username=username)
            # user.groups.add(group)
            group.user_set.add(user)
        return Response('ok')

    # 删除用户组
    if request.method == "DELETE":
        token = request.POST['token']
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        name = request.POST['name']

        gourp = Group.objects.get(name=name)
        gourp.delete()
        return Response('ok')

    # 新建用户组
    if request.method == "PUT":
        token = request.POST['token']
        permList = [
            'auth.add_user',
            'auth.delete_user',
            'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        new_name = request.POST['new_group']
        perm_list = json.loads(request.POST['perm_list'])

        new_group = Group.objects.filter(name=new_name)
        if new_group:
            return Response('same name')
        new_group = Group.objects.create(name=new_name)

        for perm in perm_list:
            app_str = perm['content_type'].split('_')[0]
            model_str = perm['content_type'].split('_')[1]
            contentType = ContentType.objects.get(
                app_label=app_str, model=model_str)
            for method in perm['perm_methods']:
                print(method)
                codename = method+'_'+model_str
                permission = Permission.objects.get(
                    content_type=contentType, codename=codename)
                new_group.permissions.add(permission)
        return Response('ok')


# 检查用户登录与权限
def userLoginAndPerm(token, permList):
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for perm_str in permList:
            perm_user = user.has_perm(perm_str)
            if perm_user:
                return 'perm_pass'
            else:
                return 'noperm'
    else:
        return 'nologin'


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def dweb_lanmu(request):
    if request.method == "GET":
        lanmu = Lanmu.objects.filter(belong=None)

        lanmu_data = loopGetLanmu(lanmu)
        return Response(lanmu_data)

    if request.method=="DELETE":
        token = request.POST['token']
        permList = [
            'blog.delete_lanmu'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        
        lanmu_id = request.POST['id']

        lanmu = Lanmu.objects.get(id=lanmu_id)
        lanmu.delete()
        return Response('ok')

    if request.method == "PUT":
        token = request.POST['token']
        permList = [
            'blog.add_lanmu',
            'blog.delete_lanmu',
            'blog.change_lanmu',
            'blog.view_lanmu'
        ]
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        lanmu_tree = json.loads(request.POST['lanmu_tree'])

        print(lanmu_tree)
        loopSaveLanmu(lanmu_tree, None)
        return Response('ok')

# 循环获取栏目数据
def loopGetLanmu(lanmu_list):
    lanmu_data = []
    for lanmu in lanmu_list:
        lanmu_item = {
            "id": lanmu.id,
            "label": lanmu.name,
            "children": [],
            "article_num":len(lanmu.article_lanmu.all())
        }
        children = lanmu.lanmu_children.all()
        print(lanmu)
        print(children)
        if children:
            children_data = loopGetLanmu(children)
            for c in children_data:
                lanmu_item['children'].append(c)
        lanmu_data.append(lanmu_item)
    return lanmu_data


# 循环保存栏目树形结构
def loopSaveLanmu(tree_data, parent_id):
    parent_lanmu = Lanmu.objects.filter(id=parent_id)
    if parent_lanmu:
        for tree in tree_data:
            saved_lanmu = Lanmu.objects.filter(id=tree['id'])
            if saved_lanmu:
                saved_lanmu[0].belong = parent_lanmu[0]
                saved_lanmu[0].save()
                if len(tree['children']) > 0:
                    loopSaveLanmu(tree['children'], saved_lanmu[0].id)
            else:
                new_lanmu = Lanmu(name=tree['label'], belong=parent_lanmu[0])
                new_lanmu.save()
                if len(tree['children']) > 0:
                    loopSaveLanmu(tree['children'], new_lanmu.id)
    else:
        for tree in tree_data:
            saved_lanmu = Lanmu.objects.filter(id=tree['id'])
            if saved_lanmu:
                saved_lanmu[0].belong = None
                saved_lanmu[0].save()
                loopSaveLanmu(tree['children'], saved_lanmu[0].id)
            else:
                new_lanmu = Lanmu(name=tree['label'])
                new_lanmu.save()
                if len(tree['children']) > 0:
                    loopSaveLanmu(tree['children'], new_lanmu.id)

    return
