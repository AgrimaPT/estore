from django.shortcuts import render,redirect
from .models import * 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UserUpdateForm,PasswordUpdateForm,UserInfoForm
from django import forms
from django.http import HttpResponse
# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})

def login_user(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged In")
            return redirect('index')
        else:
            messages.success(request,('Enter valid username and password'))
            return redirect('login')
    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Logged out"))
    return redirect('index')

def register_user(request):
    form=SignUpForm()
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,('Registered successfully. Add your user info.'))
                return redirect('info_update')
        else:
            #if form is not valid show error message
            messages.success(request,("Try again."))
        #return redirect('register')
            
    return render(request,'register.html',{'form':form})


def password_update(request):
    if request.user.is_authenticated:
        current_user=request.user
        if request.method=='POST':
            form=PasswordUpdateForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Password updated.")
                login(request,current_user)
                return redirect('user_update')
            else:
                for error in list(form.errors.values()):
                    messages.success(request,error)
                    return redirect('password_update')
        else:
            form=PasswordUpdateForm(current_user)
            return render(request,"password_update.html",{'form':form})
    else:
        messages.success(request,"You should login")

def user_update(request):
    user_form=UserUpdateForm()
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form=UserUpdateForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()
            
            login(request,current_user)
            messages.success(request,"profile updated")
            return redirect('index')
        return render(request,"user_update.html",{'user_form':user_form})
    else:
        messages.success(request,"Login to update")
        return redirect('index')
    #return render(request,'user_update.html')

def info_update(request):
    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        form=UserInfoForm(request.POST or None,instance=current_user)

        if form.is_valid():
            form.save()
            
            messages.success(request,"Your info updated")
            return redirect('index')
        return render(request,"info_update.html",{'form':form})
    else:
        messages.success(request,"Login to update")
        return redirect('index')
    #return render(request,'user_update.html')


def product(request,id):
    product=Product.objects.get(id=id)
    return render(request,'product.html',{'product':product})

#     return render(request,'nav.html',{'category':category})
def category_list(request):
    category=Category.objects.all()
    return render(request,'category_list.html',{'category':category})

def category(request,chr):
    #replace hyphens with spaces
    chr=chr.replace('-',' ')
    try:
        category=Category.objects.get(name=chr)
        products=Product.objects.filter(category=category)
        return render(request,'category.html',{'products':products,'category':category})
    except:
        messages.success(request,('Doesnt exist'))
        return redirect('index')
    
def search(request):
    products=[]
    p_count=0
    if "keyword" in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.filter(description__icontains=keyword,name__icontains=keyword) | Product.objects.filter(category__name__icontains=keyword) 
            #category is a foreign field

            p_count=products.count()
        context={
            'products':products,
            'p':p_count
        }
    return render(request,'index.html',context)
    
