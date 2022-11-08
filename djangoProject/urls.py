
"""Django01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.shortcuts import HttpResponse
from djangoProject.views import *

import pymysql


# 登录页面
# def login(request):
#     # 指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
#     return render(request, 'login_old.html')
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = User.objects.filter(username__exact=username, password__exact=password)
    #         if user:
    #             # 将username写入session，存入服务器
    #             request.session['username'] = username
    #             return HttpResponseRedirect('/index/')
    #         else:
    #             return HttpResponseRedirect('/login/')
    # else:
    #     form = LoginForm()
    #
    # return render(request, 'login_old.html', {'form': form})


# def index(request):
#     # 获取session中username
#     # username = request.session.get('username', '')
#     # if not username:
#     #     return HttpResponseRedirect('/login/')
#     # return render(request, 'index.html', {'username': username})
#     return render(request, 'home.html')

# 注册页面
# def register(request):
#     return render(request, 'register_old.html')
# def register(request):
#      """
#  3            用户注册
#  4        本视图需要对get和post请求做分别的处理
#  5        post请求
#  6            1. 从POST请求中获取数据（username，pwd)
#  7            2. 对数据进行判空
#  8            3. 判断数据库有没有重复的用户名
#  9            4. 写入数据库
# 10            5. 写入cookie
# 11            6. 跳转个人中心
# 12        get请求
# 13            返回注册页面
# 14        :param request:
# 15        :return:
# 16        """
#      if request.method == "POST":
#          uname = request.POST.get('usernamekey')  # 获取post数据
#          pwd = request.POST.get('passwordkey')
#          print(uname, pwd)
#          if not all([uname, pwd]):  # 判空
#              return HttpResponse("缺少用户名或密码")
#          # User.objects.create(username=uname, password=pwd)  # 创建
#          # res = redirect("/page")
#          # request.session["username"] = uname
#          # return res
#          try:
#              users = User.objects.filter(username=uname)
#          except Exception as e:
#              return HttpResponse("数据库查询失败")
#          if users:
#              return HttpResponse("用户名重复")
#          try:
#              User.objects.create(username=uname, password=pwd)
#          except Exception as e:
#              return HttpResponse("数据库写入失败")
#          res = redirect("/page")
#          res.set_cookie("name", uname)
#          request.session["username"] = uname
#          return res
#      return render(request, "register_old.html")

# def logout(request):
#     # try:
#     #     del request.session['username']
#     # except KeyError:
#     #     pass
#     return HttpResponse("You're logged out.")

# 定义一个函数，用来保存注册的数据
# def save(request):
#     has_register = 0  # 用来记录当前账号是否已存在，0：不存在 1：已存在
#     a = request.GET  # 获取get()请求
#     # print(a)
#     # 通过get()请求获取前段提交的数据
#     userId = a.get('userid')
#     userName = a.get('username')
#     passWord = a.get('password')
#     # print(userName,passWord)
#     # 连接数据库
#     db = pymysql.connect(db='FamiOwl', user='dev', passwd='FamiOwl123', host='cs431-06.cs.rutgers.edu', port=3306)
#
#     # 创建游标
#     cursor = db.cursor()
#     # SQL语句
#     sql1 = 'select * from parents'
#     # 执行SQL语句
#     cursor.execute(sql1)
#     # 查询到所有的数据存储到all_users中
#     all_users = cursor.fetchall()
#     i = 0
#     while i < len(all_users):
#         if userName in all_users[i]:
#             ##表示该账号已经存在
#             has_register = 1
#
#         i += 1
#     if has_register == 0:
#         # 将用户名与密码插入到数据库中
#         sql2 = 'insert into parents(parent_id,user_name,password) values(%s,%s,%s)'
#         cursor.execute(sql2, (userId,userName, passWord))
#         db.commit()
#         cursor.close()
#         db.close()
#         return render(request, 'home.html')
#     else:
#
#         cursor.close()
#         db.close()
#         return HttpResponse('This User Name Already Exist')


# def query(request):
#     a = request.GET
#     userId = a.get('userid')
#     # userName = a.get('username')
#     passWord = a.get('password')
#     # user_tup = (userId, userName, passWord)
#     user_tup = (userId, passWord)
#     db = pymysql.connect(db='FamiOwl', user='dev', passwd='FamiOwl123', host='cs431-06.cs.rutgers.edu', port=3306)
#     cursor = db.cursor()
#     sql = 'select parent_id, password from parents'
#     cursor.execute(sql)
#     all_users = cursor.fetchall()
#     cursor.close()
#     db.close()
#     has_user = 0
#     i = 0
#     while i < len(all_users):
#         if user_tup == all_users[i]:
#             has_user = 1
#         i += 1
#     if has_user == 1:
#         return HttpResponse(('Login Success'))
#     else:
#         return render(request, 'login_old.html')
#
# def index(request):
#     # 读取客户端请求携带的cookie，如果不为空，表示为已登录帐号
#     username = request.COOKIES.get('username', '')
#     if not username:
#         return HttpResponseRedirect('/login/')
#     return render(request, 'index.html', {'username': username})
# urlpatterns = [
#     path('admin/', admin.site.urls),  # 系统默认创建的
#     path('login/', login, name = 'login'),  # 用于打开登录页面
#     path('register/', register,  name = 'register'),  # 用于打开注册页面
#     path('register/save', save),  # 输入用户名密码后交给后台save函数处理
#     path('login/query', query),  # 输入用户名密码后交给后台query函数处理
#     path('', index, name = 'home')
# ]
urlpatterns = [
    path('admin/', admin.site.urls),  # 系统默认创建的
    path('register/', register,  name = 'register'),  # 用于打开注册页面
    path('login/', sign, name = 'signin'),  # 用于打开登录页面
    path('logout/', logout, name = 'logout'),
    # path('register/save', save),  # 输入用户名密码后交给后台save函数处理
    # path('login/query', query),  # 输入用户名密码后交给后台query函数处理
    path('', page, name = 'home')
]


