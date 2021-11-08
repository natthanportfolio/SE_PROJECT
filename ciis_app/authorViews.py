from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from ciis_app.models import *
from ciis_app.resource import DataCIISResource
from tablib.core import Dataset
import datetime

from django.core.files.storage import FileSystemStorage



def author_home(request):
    return render(request,"author_templates/author_home.html")

def author_add_paperid(request):
    data = paperauthor.objects.filter(email_add=request.user)
    print(data)
    return render(request,"author_templates/author_add_paperid.html",{"data":data})   

def author_addpaperid_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        paperid=request.POST.get("PaperID")
        papertitle=request.POST.get("PaperTitle")
        data=DataCIIS.objects.all()
        user=request.user
        name=paperauthor.objects.values_list('paper_id',flat=True)

        try:
            for i in data:
                if paperid == i.paper_id and papertitle == i.paper_title:
                    if paperid in name:
                        raise ValueError()
                    paper_type=i.paper_type
                    author_name=i.author_name
                    status=""

                    db=paperauthor(paper_id=paperid,paper_title=papertitle,author_name=author_name,paper_type=paper_type,email_add=user,status=status)
                    db.save()
                    messages.success(request,"Successfully")
                    return HttpResponseRedirect(reverse("author_add_paperid"))
            raise ValueError()

        except ValueError:
            messages.error(request,"This Paper ID can't be added")
            return HttpResponseRedirect(reverse("author_add_paperid"))
        except:
            return HttpResponseRedirect(reverse("author_add_paperid"))

def author_payment_history(request):
    data = Paymentpaper.objects.filter(email_add = request.user)

    return render(request,"author_templates/author_payment_history.html",{"data":data})

def author_choose_paper(request):
    data = paperauthor.objects.filter(email_add=request.user)
    return render(request,"author_templates/author_choose_paper.html",{"data":data})

def author_bill(request):
    '''
    a = paperauthor.objects.all()
    b = len(a)-1
    c = a[b].paper_id
    data = Paymentpaper.objects.filter(paper_id=c)
    '''
    data = Paymentpaper.objects.all()
    for i in data:
        d = i

    return render(request,"author_templates/author_bill.html",{"d":d})

def author_bill_save(request,paper_id):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        author_type=request.POST.get("title")
        data = paperauthor.objects.filter(paper_id=paper_id)
        paper_title = data[0].paper_title
        author_name = data[0].author_name
        paper_type = data[0].paper_type
        email_add = data[0].email_add
        status = "Overdue"

        data2 = Authors.objects.filter(admin_id=request.user.id)
        phoneno = data2[0].phoneno
        passportid = data2[0].passportid

        TODAY_CHECK = datetime.datetime.now()
        start = datetime.datetime.strptime("31-1-2021", "%d-%m-%Y")
        if TODAY_CHECK <= start:
            last_payment = "29-1-2021"
            if paper_type == "full":
                if author_type == "Regular":
                    price =  "10000"
                else:
                    price = "6000"
            else:
                if author_type == "Regular":
                    price =  "5000"
                else:
                    price = "3000"
        else:
            last_payment = "21-2-2021"
            if paper_type == "full":
                if author_type == "Regular":
                    price =  "12000"
                else:
                    price = "8000"
            else:
                if author_type == "Regular":
                    price =  "7000"
                else:
                    price = "5000"
        
        a = Paymentpaper.objects.all()
        try:
            #print(paper_id,author_type)
            for i in a:
                if paper_id == i.paper_id and author_type == i.author_type:
                    raise Exception()

            db = Paymentpaper(
            paper_id=paper_id,
            paper_title=paper_title,
            fname=request.user.first_name,
            lname=request.user.last_name,
            paper_type=paper_type,
            author_type=author_type,
            price=price,
            email_add=email_add,
            status=status,
            phoneno=phoneno,
            passportid=passportid)

            db.save()
            return redirect("author_payment_history")


        except Exception as e:
            messages.error(request,"Failed")
            return HttpResponseRedirect(reverse("author_choose_paper"))
    

def author_upload_payment(request):
    data = Paymentpaper.objects.filter(email_add = request.user).exclude(status="Success").exclude(status="").exclude(status="Downgrade").exclude(status="Upgrade")

    return render(request,"author_templates/author_upload_payment.html",{"data":data})

def update_profile_image(request,bill_id):
    if request.method == 'POST':
        profile_img = request.FILES['profile_img']

        fs=FileSystemStorage(location='media/img/')
        filename = fs.save(profile_img.name,profile_img)

    
        try:
            data = Paymentpaper.objects.get(pk=bill_id)
            data.status = "Wait verify"
            data.save()

            messages.success(request,"Upload Successfully")
            return redirect('/author_upload_payment')
        except Exception as e:
            print(e)
            messages.error(request,"Upload Failed")
            return redirect('/author_upload_payment')   
    else:
        messages.error(request,"Failed")
        return redirect('/author_upload_payment')


def author_change_status(request):
    data = Paymentpaper.objects.filter(email_add = request.user,status="Success").exclude(status="Upgrade").exclude(status="Downgrade")
        
    return render(request,"author_templates/author_change_status.html",{"data":data})

def author_change_status_save(request,bill_id):
    #print(bill_id)
    data = Paymentpaper.objects.get(pk = bill_id)

    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        try:

            TODAY_CHECK = datetime.datetime.now()

            if data.author_type == "Regular":       #downgrade
                
                data.status = "Downgrade"
                data.author_type = "Virtual"
                data.datetime = TODAY_CHECK
                data.save()

            else:                                   #Upgrade
                data.status = "Upgrade"
                data.save()
                paper_id = data.paper_id
                paper_title = data.paper_title
                fname = data.fname
                lname = data.lname
                paper_type = data.paper_type
                email = data.email_add
                status ="Overdue"
                old_price = int(data.price)
                phoneno = data.phoneno
                passportid = data.passportid
                author_type = "Regular"

                start = datetime.datetime.strptime("31-1-2021", "%d-%m-%Y")
                
                if TODAY_CHECK <= start:            #Early
                    if paper_type == "full":
                        price = 10000-old_price
                        price = str(price)
                    else:
                        price = 5000-old_price
                        price = str(price)
                else:                               #After
                    if paper_type == "full":
                        price = 12000-old_price
                        price = str(price)
                    else:
                        price = 7000-old_price
                        price = str(price)
                        

                db = Paymentpaper(
                paper_id=paper_id,
                paper_title=paper_title,
                fname=fname,
                lname=lname,
                paper_type=paper_type,
                author_type=author_type,
                price=price,
                email_add=email,
                status=status,
                phoneno=phoneno,
                passportid=passportid)

                db.save()
                data.delete()
            return redirect("author_payment_history")


        except Exception as e:
            print(e)
            messages.error(request,"Failed")
            return render(request,"author_templates/author_change_status.html")

def author_edit(request):
    data = CustomUser.objects.get(username=request.user)
    data2 = Authors.objects.get(admin_id=data.id)
    return render(request,"author_templates/author_edit.html",{"data":data,"data2":data2})

def author_edit_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        firstname=request.POST.get("first_name")
        lastname=request.POST.get("last_name")
        phoneno=request.POST.get("phone_no")
        try:
            data = CustomUser.objects.get(username=request.user)
            data2 = Authors.objects.get(admin_id=data.id)

            user = CustomUser.objects.get(id=data.id)  
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            user = Authors.objects.get(id=data2.id)  
            user.phoneno = phoneno
            user.save()

            messages.success(request,"Successfully Edited")
            return render(request,"author_templates/author_edit.html")

        except:
            messages.error(request,"Failed")
            return render(request,"author_templates/author_edit.html")
    


from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic import DetailView

class PDFUserDetailView(PDFTemplateResponseMixin, DetailView):
    model = Paymentpaper
    context_object_name='obj'
    template_name = 'pdf_detail.html'

