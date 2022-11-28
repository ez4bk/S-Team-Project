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

        if not all([user_id, uname, pwd]):  # 判空
            messages.info(request, 'Please enter your email/username/password')
            return redirect('register')

        try:
            users = User.objects.filter(user_name=uname)
        except Exception as e:
            return HttpResponse("Failed to search from database")
        if users:
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


def sign(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        if not all([user_id, password]):
            messages.info(request, 'Please enter your username/password')
            return redirect('signin')

        try:
            users = User.objects.filter(user_id=user_id)
        except Exception as e:
            return HttpResponse("Failed to connect to database")

        if users.count():
            user = users.first()
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
                    Children.objects.filter(parent_id=user_id, kids_name=kid.kids_name).update(
                        time_limit=new_time_limit)
                except Exception as e:
                    messages.info(request, 'Please input a valid number')
                    return render(request, 'my_children.html', {'kids': kids})
        kids = Children.objects.filter(parent_id=user_id)
        return render(request, 'my_children.html', {'kids': kids})
    else:
        return render(request, 'my_children.html', {'kids': kids})


def my_profile(request):
    user_id = request.session.get("user_id")
    try:
        users = User.objects.filter(user_id=user_id)
    except Exception as e:
        return HttpResponse("Failed to connect to database")
    if users.count():
        user = users.first()
        return render(request, 'my_profile.html', {'user': user})
    else:
        return HttpResponse('Could not get user information')


def about_us(request):
    return render(request, 'about_us.html')


def page(request):
    uname = request.session.get("user_id")

    if not uname:
        messages.info(request, 'Now you are a guest, please login/sign up')
        return render(request, 'guest_home.html')
    messages.info(request, 'Welcome to FamiOwl, ' + str(uname))
    return render(request, 'user_home.html')
