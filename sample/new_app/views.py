from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as authlogin,logout as authlogout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


#Sign up page
@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST:
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.warning(request,'Username exists')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email exists')
            return redirect('signup')
        
        if len(password1)<8:
            messages.warning(request,'Password must be greater than 8 characters')
            return redirect('signup')
        
        if password1!=password2:
            messages.warning(request,'Passwords do not match')
            return redirect('signup')
        
        
        user=User.objects.create_user(username,email,password1)
        user.save()
        return redirect('login')
    return render(request,'signup.html')

#Login page
@never_cache
def login(request):
    error_message=None
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            authlogin(request,user)
            return redirect('home')
        else:
            error_message='Invalid username or password'

    return render(request,'login.html',{'error_message':error_message})

#Home page
@never_cache
@login_required(login_url='login')
def home(request):
   if request.user.is_authenticated:
       if request.user.is_superuser:
           return redirect('myadmin')
       return render(request,'home.html',{'user':request.user})
   return redirect('login')

#Logout
@login_required(login_url='/')
def logout(request):
    authlogout(request)
    return redirect('login')

#Admin page
@never_cache
def myadmin(request):
   if request.user.is_superuser:
       user=User.objects.all().order_by('-date_joined')
       return render(request,'myadmin.html',{'users':user})
   return redirect('login')

#Add user
@login_required(login_url='/')
def adduser(request):
    if request.POST:
        name=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if User.objects.filter(username=name).exists():
            messages.warning(request,'Username exists')
            return redirect('myadmin')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email exists')
            return redirect('myadmin')
        
        if len(password1)<8:
            messages.warning(request,'Password must be greater than 8 characters')
            return redirect('myadmin')
        
        if password1!=password2:
            messages.warning(request,'Passwords do not match')
            return redirect('myadmin')
        
        
        user=User.objects.create_user(username=name,email=email,password=password1)
        user.save()
        return redirect('myadmin')
    
    
#Edit user
@login_required(login_url='/')
def edituser(request,id):
    user= get_object_or_404(User,id = id)
    if request.POST:
        name=request.POST['username']
        email=request.POST['email']
        if User.objects.filter(username=name).exists():
            messages.warning(request,'Username exists')
            return redirect('myadmin')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email exists')
            return redirect('myadmin')
        user.username=name
        user.email=email
        user.save()
        return redirect('myadmin')
    
#Delete user
@login_required(login_url='/')
def deleteuser(request,id):
    if request.POST:
        del_user = User.objects.get(id=id)
        del_user.delete()

    return redirect(myadmin)

#Search user
@login_required(login_url='/')
def searchuser(request):
     if request.POST:
        user_details = request.POST.get('search')
        if user_details:
            user = User.objects.filter(username=user_details).order_by('username')
        else:
            user = User.objects.all()  
        return render(request,'myadmin.html',{'users':user})
    
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
# @login_required(login_url='login')
def Homepage(request):
    return render(request, 'home.html')


@never_cache
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to homepage after successful login
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
