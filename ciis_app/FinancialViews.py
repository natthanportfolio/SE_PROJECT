from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from ciis_app.models import *
from django.db.models import Q


def financial_home(request):
    data = Paymentpaper.objects.all().exclude(status="Overdue").exclude(status="Wait verify")
    tmb = 0
    paypal = 0
    pp = 0
    for i in data:
        j = int(i.price)
        if(j < 500):
            paypal += j
        else:
            tmb += j
    total = tmb + paypal*30

    data2 = Memberparticipant.objects.filter(status ="Success")
    for i in data2:
        pp += i.price
    

    return render(request,"financial_templates/home_content.html",{"total":total,"tmb":tmb,"paypal":paypal,"pp":pp,"s":pp+total})
    

def financial_approval_history_author(request):
    approvalauthor=Approvalauthor.objects.all()
    return render(request,"financial_templates/financial_approval_history_author.html",{"approvalauthor":approvalauthor})

def financial_approval_history_Participant(request):
    approvalpp=Approvalpp.objects.all()
    return render(request,"financial_templates/financial_approval_history_Participant.html",{"approvalpp":approvalpp})

# 
def financial_payment_update_author(request):
    paymentpaper=Paymentpaper.objects.filter(status ="Wait verify")
    return render(request,"financial_templates/financial_payment_update_author.html",{"paymentpaper":paymentpaper})
# 
def cancel_statusat(request, id):
    obj = Paymentpaper.objects.get(pk = id)
    obj.status="Overdue"
    obj.save()
    messages.success(request,"Cancel Success")
    return redirect('financial_payment_update_author')
# 
def success_statusat(request, id):
    obj = Paymentpaper.objects.get(pk = id)
    obj.status="Success"
    obj.save()
    messages.success(request,"Success")
    return redirect('financial_payment_update_author')
    
# 
def financial_payment_update_Participant(request):
    payhistorypp = Memberparticipant.objects.filter(status ="Wait verify")
    return render(request,"financial_templates/financial_payment_update_Participant.html",{"payhistorypp":payhistorypp})

def cancel_statuspp(request, id):
    obj = Memberparticipant.objects.get(pk = id)
    obj.status="Overdue"
    obj.save()
    messages.success(request,"Cancel Success")
    return redirect('financial_payment_update_Participant')

def success_statuspp(request, id):
    obj = Memberparticipant.objects.get(pk = id)
    obj.status="Success"
    obj.save()
    messages.success(request,"Success")
    return redirect('financial_payment_update_Participant')


    
def financial_status_change_request_author(request):
    paymentpaper=Paymentpaper.objects.filter(status ="Success")
    return render(request,"financial_templates/financial_status_change_request_author.html",{"paymentpaper":paymentpaper})

def change_statusat(request, id):
   
    check = Approvalauthor.objects.values_list('billid',flat=True)
    for i in check:
        if i == id :
            messages.error(request,"Please contact the admin")
            return redirect('financial_status_change_request_author')
           
        
    obj =Paymentpaper.objects.get(pk = id)
    obj.status="Error"
    obj.save()
    req1=Approvalauthor.objects.create(billid=obj.bill_id,
    papertitle=obj.paper_title,
    price=obj.price,
    editby=str(request.user),
    statusapproval="Waiting for approval")
    req1.save()
    messages.success(request,"Success")
    return redirect('financial_status_change_request_author')

def financial_status_change_request_Participant(request):
    payhistorypp= Memberparticipant.objects.filter(status ="Success")
    return render(request,"financial_templates/financial_status_change_request_Participant.html",{"payhistorypp":payhistorypp})
    
def change_statuspp(request, id):
    check = Approvalpp.objects.values_list('billid',flat=True)
    for i in check:
        if i == id :
            messages.error(request,"Please contact the admin")
            return redirect('financial_status_change_request_Participant')
    obj =Memberparticipant.objects.get(pk = id)
    obj.status="Error"
    obj.save()
    req=Approvalpp.objects.create(billid=obj.id,paperlist=obj.paperlist,price=obj.price,editby=str(request.user),statusapproval="Waiting for approval")
    req.save()
    messages.success(request,"Success")
    return redirect('financial_status_change_request_Participant')