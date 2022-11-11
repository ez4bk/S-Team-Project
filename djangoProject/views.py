from django.shortcuts import render, HttpResponse, redirect
from djangoProject.models import *
from djangoProject.aes_pass import *
from django.contrib import messages

aes_pass = AESCipher()


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
        # print(uname, pwd)
        if not all([user_id, uname, pwd]):  # 判空
            messages.info(request, 'Please enter your email/username/password')
            return redirect('register')
        # User.objects.create(username=uname, password=pwd)  # 创建
        # res = redirect("/page")
        # request.session["username"] = uname
        # return res
        try:
            users = User.objects.filter(user_name=uname)
        except Exception as e:
            return HttpResponse("Failed to search from database")
        if users:
            # messages.warning(request, 'Username already exists')
            messages.info(request, 'Username already exists')
            return redirect('register')
        try:
            User.objects.create(user_name=uname, password=aes_pass.encrypt_main(pwd), user_id=user_id)
        except Exception as e:
            return HttpResponse("Failed to write to database")
        res = redirect("register")
        res.set_cookie("id", user_id)
        request.session["user_id"] = user_id
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
            messages.info(request, 'Please enter your username/password')
            return redirect('signin')
        # 密码
        try:
            users = User.objects.filter(user_id=user_id)
        except Exception as e:
            return HttpResponse("Failed to connect to database")
        # 查看 User 表有没有 username
        if users.count():
            # .count 也可以写为 .exists,直接判断是否存在
            #     有就是 1  , 没有就是 0
            # user 用户存在
            user = users.first()
            #     取数据  last() 也可以
            # print(type(user.password))
            # print(type(aes_pass.decrypt(user.password)))
            print()
            if password == aes_pass.decrypt_main(user.password):
                res = redirect("/")
                res.set_cookie("id", user_id)
                request.session["user_id"] = user_id
                return res
            else:
                messages.warning(request, 'Wrong password')
                return redirect('signin')
        else:
            messages.warning(request, 'Username not found')
            redirect('signin')
            # print("用户名不存在")
            # uname = request.session.get("user_id", None)
            # uuname = request.COOKIES.get("id", None)
            # print(uname)
            # if uname:
            #     return redirect("/")
            # elif uuname:
            #     return redirect("/")
    return render(request, "signin.html")


def logout(request):
    res = redirect("/")
    res.delete_cookie('id')
    request.session.delete()
    return res


def my_children(request):
    user_id = request.session.get("user_id")
    kids = Children.objects.filter(parent_id=user_id)
    if kids.count() == 0:
        messages.warning(request, 'Please sign up for your kids')
        return render(request, 'my_children.html')

    if request.method == 'POST':
        for kid in kids:
            if kid.kids_name in request.POST:
                new_time_limit = request.POST.get(kid.kids_name)
                try:
                    Children.objects.filter(parent_id=user_id, kids_name=kid.kids_name).update(time_limit=new_time_limit)
                except Exception as e:
                    messages.info(request, 'Please input a valid number')
                    return render(request, 'my_children.html',{'kids': kids})
        kids = Children.objects.filter(parent_id=user_id)
        return render(request, 'my_children.html', {'kids': kids})
    else:
        return render(request, 'my_children.html', {'kids': kids})


    # user_id = request.session.get("user_id")
    # new_time_limit = request.POST.get('time_limit')
    # # kids = Children.objects.filter(parent_id=user_id)
    # try:
    #     kids = Children.objects.filter(parent_id=user_id)
    # except Exception as e:
    #     return HttpResponse("Failed to connect to database")
    #
    # if kids.count():
    #     # temp = Children.objects.get(parent_id=user_id)
    #     for kid in kids:
    #         temp = Children.objects.get(parent_id=user_id,kids_name = kid.kids_name)
    #
    #         temp.time_limit = new_time_limit
    #         temp.save()
    #     # Children.objects.filter(parent_id=user_id).update(time_limit=new_time_limit)
    # else:
    #     try:
    #         User.objects.create(parent_id=user_id, time_limit=new_time_limit)
    #     except Exception as e:
    #         return HttpResponse("Failed to write to database")
    #
    # return render(request, 'my_children.html', {'kids':kids})

# def set_time_limit(request):
#     user_id = request.session.get("user_id")
#     new_time_limit = request.POST.get('time_limit')
#     try:
#         kids = Children.objects.filter(parent_id=user_id)
#     except Exception as e:
#         return HttpResponse("Failed to connect to database")
#
#     if kids.count():
#         kids = Children.objects.get(parent_id=user_id)
#         for kid in kids:
#             kid.time_limit = new_time_limit
#             kid.save()
#     else:
#         try:
#             User.objects.create(parent_id=user_id, time_limit=new_time_limit)
#         except Exception as e:
#             return HttpResponse("Failed to write to database")


def page(request):
    """
42     页面
43     1.获取session进行判断
44     2.存在正常进入，不存在返回注册界面
45     :param request:
46     :return:
47     """
    uname = request.session.get("user_id")
    # print(uname)
    if not uname:
        messages.info(request, 'Now you are a guest, please login/sign up')
        return render(request, 'guest_home.html')
    messages.info(request, 'Welcome to FamiOwl, ' + str(uname))
    return render(request, 'user_home.html')
