from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotModified
from django.contrib.auth import login, logout, logout
from ciis_app.EmailBackEnd import EmailBackEnd
from django.urls import reverse
from django.contrib import messages
from ciis_app.models import *
from ciis_app import forms
from ciis_app.resource import DataCIISResource
from tablib.core import Dataset
from django.core.mail import EmailMessage
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator
from django.views import View
import datetime


def showLoginPage(request):
    return render(request,"login_page.html")

def showIndex(request):
    return render(request,"home.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            b=request.user.id
            t=request.user.user_type
            d = ""
            if t== "3": 
                c=Authors.objects.filter(admin_id=b) 
                d=str(c[0].status)
            if user.user_type == "1":
                return HttpResponseRedirect('/manages')
            elif user.user_type == "2":
                return HttpResponseRedirect('/financial_home')
            elif user.user_type == "3" and d=="authorthai":
                return HttpResponseRedirect('/author_payment_history')
            elif user.user_type == "3" and d=="authorforeigner":
                return HttpResponseRedirect('/authorf_payment_history')
            elif user.user_type == "4":
                return HttpResponseRedirect('/participant_payment_history')

            else:
                return HttpResponseRedirect(reverse("admin"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def Logout(request):
    logout(request)
    #แจ้งว่าlogoutแล้ว แก้ messageได้
    messages.info(request, "Logged out successfully!")
    return redirect('/')


def doRegister(request):
    return render(request,"register.html")


def register_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        title=request.POST.get("title")
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        phone_number=request.POST.get("phonenum")
        passport_id=request.POST.get("ppID")
        affiliation=request.POST.get("affiliation")
        country=request.POST.get("contrys")
        nationality=request.POST.get("nationality")
        status=request.POST.get("drone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")

        try:
            if password == cpassword:
                pw = password
                
            else:
                raise e
            
            if status == "Participant":
                status = "pp"
                u_type = 4
            else:
                if country == "thai":
                    status = "authorthai"
                    u_type = 3

                else:
                    status = "authorforeigner"
                    u_type = 3

            
            user = CustomUser.objects.create_user(username=email,password=password,email=email,last_name=last_name,first_name=first_name,user_type=u_type)
            
            if u_type == 3:
                user.authors.phoneno=phone_number
                user.authors.passportid=passport_id
                user.authors.affiliation=affiliation
                user.authors.country=country
                user.authors.nationality=nationality
                user.authors.status=status
            elif u_type == 4:
                user.participants.phoneno=phone_number
                user.participants.passportid=passport_id
                user.participants.affiliation=affiliation
                user.participants.country=country
                user.participants.nationality=nationality
                user.participants.status=status
                
            user.is_active = False
            user.save()

            #Send email
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            
            domain = get_current_site(request).domain
            link=reverse('activate',kwargs={
                'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = 'http://'+domain+link
            email_subject='Activate your account '
            email_body='Hi'+user.username + \
                'Please use this link\n' + activate_url
            email = EmailMessage(email_subject,email_body,
            'noreply@example.com',[email],)

            email.send(fail_silently=False)

            messages.success(request,"Register Success")

            return HttpResponseRedirect(reverse("Logout"))

        except Exception as e:
            print(e)
            messages.error(request,"Failed")
            return HttpResponseRedirect(reverse("doRegister"))




class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)
            user.is_active = True
            user.save()
            if user.is_active:
                return redirect('/')
            messages.success(request, 'Account activated successfully')
            return redirect('/')

        except Exception as ex:
            pass

        return redirect('/')



class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'reset-password.html')
    def post(self,request):
        email= request.POST['email']
        
        context = {
            'values':request.POST
        }
        user=CustomUser.objects.filter(email=email)

        if email=="" or not user:
            messages.error(request,'Email wrong!!!')
            return render(request,'reset-password.html')

        current_site = get_current_site(request)

        email_contents={
            'user':user[0],
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
            'token':PasswordResetTokenGenerator().make_token(user[0])
            }
        


        link=reverse('reset-user-password',kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']
            })

        reset_url = 'http://'+current_site.domain+link
        email_subject='Password Reset'
        email_body='Hi there Please the click link below to reset your password\n' + reset_url
        email = EmailMessage(
        email_subject,
            email_body,
            'noreply@example.com',
            [email],
            )
        email.send(fail_silently=False)
        
        messages.success(request,'Please check your email and click on the provided link to reset your password.')
       
        return render(request,'reset-password.html')

class CompletePasswordReset(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user= CustomUser.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request,'Password link is invalid,please request an new one')
                return render(request,'reset-password.html')
    
        except Exception as identifier:
            pass
        return render(request,'set-new-password.html',context)
    def post(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['password']
        password2=request.POST['password2']
        if password!= password2:
            messages.error(request,'Passwords do not match')
            return render(request,'set-new-password.html',context)
        if len(password) < 6:
            messages.error(request,'Passwords too short')
            return render(request,'set-new-password.html',context)
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user= CustomUser.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset')
            return redirect('/')
        except Exception as identifier:
            messages.info(request,'Something went wrong,try again')
            return render(request,'set-new-password.html',context)

       # return render(request,'set-new-password.html',context)       