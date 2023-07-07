from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import UserData
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseForbidden

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                return render(request, '403.html', status=403)
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator



def login_user(request):
    if request.user.is_authenticated:
        if request.user.role == 'siswa':
            return redirect('/dashboard-siswa')
        elif request.user.role == 'guru':
            return redirect('/dashboard-guru')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                user.is_login = True
                user.save()
                messages.success(request, 'Login Berhasil')
                return redirect('/login')
            else:
                messages.error(request, 'Login Gagal')
                return render(request, 'auth/login.html', {'title': 'Login'})
        else:
            return render(request, 'auth/login.html',{'title': 'Login','site_name':'Cryptos.com'})



def register_siswa(request):
    if request.user.is_authenticated:
        return redirect('/dashboard-siswa')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            fullname = request.POST['fullname']
            phone = request.POST['phone']
            user = UserData.objects.create_user(nama_lengkap=fullname, username=username, email=email, no_hp=phone, password=password,role='siswa')
            return redirect('/login')
        else:
            return render(request, 'siswa/auth/register-siswa.html',{'title': 'Register','site_name':'Cryptos.com'})
        

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_login = False
        request.user.save()
        logout(request)
        messages.success(request, 'Login Berhasil')
        return redirect('/login')
