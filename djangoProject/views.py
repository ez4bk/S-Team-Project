from django.shortcuts import render, HttpResponse, redirect
from djangoProject.models import User


def register(request):
    """
3            用户注册
4        本视图需要对get和post请求做分别的处理
5        post请求
6            1. 从POST请求中获取数据（username，pwd)
7            2. 对数据进行判空
8            3. 判断数据库有没有重复的用户名
9            4. 写入数据库
10            5. 写入cookie
11            6. 跳转个人中心
12        get请求
13            返回注册页面
14        :param request:
15        :return:
16        """
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        uname = request.POST.get('username')  # 获取post数据
        pwd = request.POST.get('password')
        print(uname, pwd)
        if not all([user_id, uname, pwd]):  # 判空
            return HttpResponse("One Element Missing")
        # User.objects.create(username=uname, password=pwd)  # 创建
        # res = redirect("/page")
        # request.session["username"] = uname
        # return res
        try:
            users = User.objects.filter(user_name=uname)
        except Exception as e:
            return HttpResponse("数据库查询失败")
        if users:
            return HttpResponse("Duplicate username")
        try:
            User.objects.create(user_name=uname, password=pwd, user_id = user_id)
        except Exception as e:
            return HttpResponse("数据库写入失败")
        res = redirect("/")
        res.set_cookie("name", uname)
        request.session["user_name"] = uname
        return res
    return render(request, "signup.html")


# def sign(request):
     # """
     # 登录
     # 1.获取网页数据（用户名，密码）
     # 2.进行用户名和密码的校验
     # :param request:
     # :return:
     # """
     # if request.method == "POST":
     #     uname = request.POST.get('user_name')  # 获取网页
     #     pwd = request.POST.get('password')
     #     if User.objects.filter(user_name=uname, password=pwd):
     #         return redirect("/")
     #     else:
     #         return HttpResponse("登录失败账号或密码错误")
     # return render(request, "signin.html")
def sign(request):

      if request.method == "POST":  # 先验证用户名是否存在再判断密码是否存在
          user_id = request.POST.get('user_id')  # 获取post数据
          password = request.POST.get('password')
          if not all([user_id, password]):  # 判空
             return HttpResponse("缺少用户名或密码")
      # 密码
          try:
              users = User.objects.filter(user_id=user_id)
          except Exception as e:
             return HttpResponse("数据库连接失败")
     # 查看 User 表有没有 username
          if users.count():
             # .count 也可以写为 .exists,直接判断是否存在
             #     有就是 1  , 没有就是 0
             # user 用户存在
             user = users.first()
             #     取数据  last() 也可以
             # print(type(user.password))
             # print(type(password))
             if password == user.password:
                 res = redirect("/")
                 res.set_cookie("id", user_id)
                 request.session["user_id"] = user_id
                 return res
             else:
                 print("Wrong Password")
          else:
             print("用户名不存在")
             uname = request.session.get("user_id", None)
             uuname = request.COOKIES.get("id", None)
             print(uname)
             if uname:
                return redirect("/")
             elif uuname:
                return redirect("/")
      return render(request, "signin.html")


def logout(request):
    request.session.delete()
    return redirect("/")

def page(request):
     """
42     页面
43     1.获取session进行判断
44     2.存在正常进入，不存在返回注册界面
45     :param request:
46     :return:
47     """
     uname = request.session.get("user_id")
     print(uname)
     if not uname:
         return redirect("/register")
     return render(request, "home.html", {"uname": uname})
