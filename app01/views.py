import os

from django.shortcuts import render, redirect

from django.http import JsonResponse
from django_redis import get_redis_connection

from Caroll.settings import BASE_DIR
from app01.forms import RegisterModelForm, SendSmsForm
from app01.models import UserInfo, UserFile
from utils import encrypt

from django.views.decorators.csrf import csrf_exempt


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def register(request):
    form = RegisterModelForm()

    if request.method == "POST":
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True, "data": "/login"})
        return JsonResponse({"status": False, "error": form.errors})
    return render(request, 'Register.html', locals())


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if all([username, password]):
            password = encrypt.md5(password)
            user = UserInfo.objects.filter(username=username, password=password).first()
            if user:
                conn = get_redis_connection()
                conn.set('username', user.id)
                return redirect('home2')
            msg = "用户名或密码错误"
        else:
            msg = "用户名或密码缺失"

    return render(request, 'Login.html', locals())


def home(request):
    return render(request, 'home.html')


def home2(request):
    return render(request, 'home2.html')


def author(request):
    return render(request, 'author.html')


def demoIndex(request):
    return render(request, 'demo_index.html')


def index(request):
    return render(request, 'index.html')


def light(request):
    return render(request, 'light.html')


def nxh(request):
    return render(request, 'NXH.html')


def pubuliu(request):
    return render(request, 'pubuliu.html')


def pubuliu2(request):
    return render(request, 'pubuliu2.html')


def pubuliu3(request):
    return render(request, 'pubuliu3.html')


def shicha(request):
    return render(request, 'shicha.html')


def maoboli(request):
    return render(request, 'maoboli.html')


def awa(request):
    return render(request, 'awa.html')


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        # 保存文件
        filename = os.path.join(BASE_DIR, 'app01/static/media', file.name)
        filepath = os.path.join('media', file.name)
        print(filepath)
        conn = get_redis_connection()
        uid = conn.get('username')
        if not uid:
            return JsonResponse({"status": False})
        uf = UserFile.objects.create(filepath=filepath, user_id=uid)
        with open(filename, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        uf.save()
        return JsonResponse({"status": True})


def personInfo(request):
    conn = get_redis_connection()
    uid = conn.get('username')

    if not uid:
        return redirect('login')
    user = UserInfo.objects.get(pk=uid)
    queryList = UserFile.objects.filter(user_id=uid)
    return render(request, 'personInfo.html', locals())


def logout(request):
    conn = get_redis_connection()
    conn.delete('username')
    return redirect('login')
