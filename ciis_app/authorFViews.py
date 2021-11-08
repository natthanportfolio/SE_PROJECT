from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render,redirect
from django.urls import reverse
from ciis_app.models import *
from ciis_app.resource import DataCIISResource
from tablib.core import Dataset
import datetime
import json


def authorf_home(request):
    return render(request,"authorf_templates/author_home.html")


def authorf_add_paperid(request):
    data = paperauthor.objects.filter(email_add=request.user)
    #print(data)
    return render(request,"authorf_templates/author_add_paperid.html",{"data":data})   


def authorf_addpaperid_save(request):

    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        paperid=request.POST.get("PaperID")
        papertitle=request.POST.get("PaperTitle")
        data=DataCIIS.objects.all()
        user=request.user
        name=paperauthor.objects.values_list('paper_id',flat=False)
        #print(name)

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
                    return HttpResponseRedirect(reverse("authorf_add_paperid"))
            raise ValueError()

        except ValueError:
            messages.error(request,"This Paper ID can't be added")
            return HttpResponseRedirect(reverse("authorf_add_paperid"))
        except:
            return HttpResponseRedirect(reverse("authorf_add_paperid"))


def authorf_payment_history(request):
    data = Paymentpaper.objects.filter(email_add=request.user)
    #print(data)
    return render(request,"authorf_templates/author_payment_history.html",{"data":data})


def authorf_choose_paper(request):
    data = paperauthor.objects.filter(email_add=request.user)
    list_result = []
    for i in data:
        #i.paper_id
        list_result.append(i.paper_id)
    #print(list_result)
    #data_type = paperauthor.value_list('paper_type',flat=True)
    return render(request,"authorf_templates/author_choose_paper.html",{"data":data})


def authorf_bill_save(request,paper_id):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        author_type = "Regular"
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
                    price =  "320"
                else:
                    price = "192"
            else:
                if author_type == "Regular":
                    price =  "160"
                else:
                    price = "97"
        else:
            last_payment = "21-2-2021"
            if paper_type == "full":
                if author_type == "Regular":
                    price =  "385"
                else:
                    price = "257"
            else:
                if author_type == "Regular":
                    price =  "225"
                else:
                    price = "160"
        data = Paymentpaper.objects.values_list('paper_id',flat=True)
        l = []

        try:
            for i in data:
                l.append(i)
            if paper_id in l:
                raise Exception()

            db = Paymentpaper(paper_id=paper_id,paper_title=paper_title,
            fname=request.user.first_name,lname=request.user.last_name,paper_type=paper_type,
            author_type=author_type,price=price,email_add=email_add,status=status,
            phoneno=phoneno,passportid=passportid)
            db.save()
            obj=paperauthor.objects.get(paper_id=paper_id)
            obj.status=status
            obj.save()

            return redirect("authorf_payment_history")

        except Exception as e:
            print(e)
            messages.error(request,"Failed")
            return HttpResponseRedirect(reverse("authorf_choose_paper"))


def authorf_upload_payment(request):
    data = Paymentpaper.objects.filter(status="Overdue")
    #print(data)
    return render(request,"authorf_templates/author_upload_payment.html",{"data":data})


def authorf_edit(request):
    data = CustomUser.objects.get(username=request.user)
    data2 = Authors.objects.get(admin_id=data.id)
    #print(data2)
    return render(request,"authorf_templates/author_edit.html",{"data":data,"data2":data2})


def authorf_edit_save(request):
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
            return render(request,"authorf_templates/author_edit.html")

        except:
            messages.error(request,"Failed")
            return render(request,"authorf_templates/author_edit.html")


def checkout(request, pk):
	product = Paymentpaper.objects.get(bill_id=pk)
	context = {'product':product}
	return render(request, 'authorf_templates/checkout.html', context)


def paymentComplete(request):
    a = json.loads(request.body)
    l=[]
    for lines in a:
        l.append(a[lines])
    print(l)
    #print("bill id : ", text)
    user = Paymentpaper.objects.get(pk=l[0])
    obj = paperauthor.objects.get(paper_id=l[1])
    TODAY_CHECK = datetime.datetime.now()
    
    try:
        user.status = "Success"
        user.datetime = TODAY_CHECK
        user.save()
        obj.status="Success"
        obj.save()

        return render(request, 'authorf_templates/author_payment_history.html')
    except:
        return render(request, 'authorf_templates/author_home.html')













            




