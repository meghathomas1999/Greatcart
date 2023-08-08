from django.shortcuts import render
from . forms import RegistrationForm
from . models import Account
from django.shortcuts import redirect
from django.contrib import messages 
from django.contrib.auth import authenticate,login
from django.contrib.auth. decorators import login_required
from django.http import HttpResponse
from django.contrib import auth

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            print("email",email)
            print("first name",first_name)
            print("last name",last_name)
            print("phone number", phone_number)
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username, 
                password=password,
                phone_number=phone_number)
            user.phone_number=phone_number
            user.save()
            #user activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid'   :urlsafe_base64_encode(force_bytes(user.pk)),
                'token' :default_token_generator.make_token(user)

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request,'Thank you for registering we have send you an verification email to your email(meghathomas1999@gmail.com) address please verify it ')
            return redirect('/accounts/login/?command=verification&email='+email)
            
    else:

       form=RegistrationForm()
    context = {
        "form" : form,

    }  
    return render(request,'accounts/register.html',context)
def user_login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        print("email",email)
        print("password",password)
        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are now login ")
            return redirect('dashboard')
        else:
            messages.error(request," Invalid login credentials ")
            return redirect('login')



    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are Loggout")
    return redirect('login')
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations your account is activated")
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')
def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #password set email
            current_site = get_current_site(request)
            mail_subject = " Reset your password "
            message = render_to_string('accounts/Reset_Password_email.html',{
                'user':user,
                'domain':current_site,
                'uid'   :urlsafe_base64_encode(force_bytes(user.pk)),
                'token' :default_token_generator.make_token(user)

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,"Password reset email has been to your email address ")
            return redirect('login')

        else:
           messages.error(request," Account doesnot exist ")
           return redirect('')
    return render (request,'accounts/forgotpassword.html')

def Reset_Password_Validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None 

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,"Please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request,"This link has been expired")
        return redirect('login')
def resetpassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset exists")
            return redirect('login')


        else:
            messages.error(request,"Your password do not match")
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')
    
