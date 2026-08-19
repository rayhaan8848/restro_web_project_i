from django.shortcuts import render, redirect
from .models import Contact,Category,Momo,Review
from django.contrib import messages
import qrcode
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from datetime import datetime




# Create your views here.
def index(request):
    category=Category.objects.all()
    cateid=request.GET.get('category')

    if cateid == 'all':
        momo=Momo.objects.filter(is_available=True)

    elif cateid:
        momo=Momo.objects.filter(is_available=True, category=cateid)
    else:
        momo=Momo.objects.filter(is_available=True)
    if request.method =='POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject="Thanks for Messaging us"
        message=render_to_string('core/mail_one.html', {'name':name, "date":datetime.now})
        from_email='rayhaankanxa@gmail.com'
        recipient_list=[email]
        send_mail(subject=subject, message=message, from_email=from_email,recipient_list=recipient_list,fail_silently=False)

        message = request.POST['message']
        Contact.objects.create(name=name, email=email, phone=phone,message=message)
        messages.success(request, f"{name} your Form successfully Submitted!!")
        response = redirect('index')
        response.set_cookie('name',name,max_age=100)
        return response
    
    context={
        'category': category,
        'momo':momo
    }
    return render(request, 'core/index.html',context)

def about(request):
    return render(request, 'core/about.html')
def contact(request):
    return render(request, 'core/contact.html')

@login_required(login_url='login')
def menu(request):
    category=Category.objects.all()
    qr=qrcode.make("http://127.0.0.1:8000/menu/")
    qr.save("core/static/images/qr.png")
    context={
        'category':category
    }
    return render(request, 'core/menu.html', context)


def services(request):
    return render(request, 'core/services.html')

from urllib.parse import quote
@login_required(login_url='testemonial')
def testemonial(request):
    momos=Momo.objects.all()
    review=Review.objects.all()
    if request.method == "POST":
        name=request.POST['name']
        message=request.POST['message']
        order=request.POST['order'] 
        rating=request.POST['rating']
        Review.objects.create(name=name,message=message,order=order,rating=rating)
        messages.success(request, f"{name} your Form successfully Submitted!!")

        # whats_app=f'''
        # Order review
        # Name : {name}
        # Order : {order}
        # rating : {rating}
        # '''
        # whats_app_url=("https://wa.me/9816107823?text="+quote(whats_app))
        # return redirect(whats_app_url)
        return redirect('testemonial')
    context={
        'momos':momos,
        'review':review
    }


    return render(request, 'core/testemonial.html',context)


'''==========================AUTH PART================================='''
def register(request):
    if request.method == "POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password == password1:
            if User.objects.filter(username = username).exists():
                messages.error(request, "username is already exists")
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.error(request, "email is already exists")
                return redirect('register')
           
            # if not re.search(r"[A-Z]",password):
            #     messages.error(request, "password must contain at least one upper case")
            #     return redirect('register')
            # if not re.search(r"\d",password):
            #     messages.error(request, "password must contain at least one one digit")
            #     return redirect('register')

            try:
                # user=User(first_name=fname,username=username)
                validate_password(password) #user=user
                User.objects.create_user(first_name=fname,last_name=lname, username=username,email=email,password=password)
                messages.success(request, "Account successfully Created")
                return redirect('register')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request, i)
                return redirect ("register")

        
        else:
            messages.error(request, "enter same password! to continue")
            return redirect('register')

    return render(request, 'auth/register.html')

def log_in(request):
    name=request.COOKIES.get('name')
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        remember_me=request.POST.get("remember_me")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "username is not registered yes")
            return redirect("login")

        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(360000)
            else:
                request.session.set_expiry(0)
            next=request.POST.get('next', '')
            return redirect(next if next else 'index')
        else:
            messages.error(request, "invaild Password")

    next=request.GET.get('next', "")
    return render(request, 'auth/login.html', {'next':next, "name":name})

def log_out(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    return render(request,"auth/password_change.html",{"form":form})

