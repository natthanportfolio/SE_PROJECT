from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from ciis_app.models import *
from ciis_app.resource import DataCIISResource
from tablib.core import Dataset

'''
export excel
'''
import csv

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MemberExhibitors.csv"'

    writer = csv.writer(response)
    writer.writerow(['Member Exhibitor'])
    writer.writerow(['Bill ID','Paper Id','Paper Title', 'First name', 'Last name', 'Email address','Type'])
   
    writer2 = csv.writer(response)
    
    users1 = Paymentpaper.objects.filter(status="Success").values_list('bill_id','paper_id','paper_title', 'fname', 'lname', 'email_add','author_type')
    users2 = Paymentpaper.objects.filter(status="Downgrade").values_list('bill_id','paper_id','paper_title', 'fname', 'lname', 'email_add','author_type')
    users3= Memberparticipant.objects.filter(status="Success").values_list('id','firstname1', 'lastname1','firstname2', 'lastname2','firstname3', 'lastname3','firstname4', 'lastname4','firstname5', 'lastname5')
    for user1 in users1:
        writer2.writerow(user1)
    for user1 in users2:
        writer2.writerow(user1)
    
    writer.writerow([''])
    writer.writerow(['Participant Member'])
    writer.writerow(['Bill_ID','First Name1', 'Last Name1','First Name2', 'Last Name2','First Name3', 'Last Name3','First Name4', 'Last Name4','First Name5', 'Last Name5'])

    for user3 in users3:
        writer2.writerow(user3)
    
    
    return response
'''
export excel
'''

def admin_home(request):
    return render(request,"admin_templates/base_template.html")
def add_financial(request):
    return render(request,"admin_templates/add_financial.html")



def add_admin(request):
    return render(request,"admin_templates/add_admin.html")

###update 11/4/2020 15.12
def add_admin_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")

        try:

            if password != cpassword:
                raise Exception("Password not match")
            
            try:
                user=CustomUser.objects.create_user(username=email,password=password,email=email,last_name=last_name,first_name=first_name,user_type=1)
            except:
                raise Exception("The email address has been taken.")
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse("add_admin"))
        else:
            user.save()
            messages.success(request,"Successfully Added Admin")
            return HttpResponseRedirect(reverse("staff_account"))


def add_financial_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        address=request.POST.get("address")
        try:
            if password != cpassword:
                raise Exception("Password not match")
            
            try:
                user=CustomUser.objects.create_user(username=email,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            except:
                raise Exception("The email address has been taken.")
        
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse("add_financial"))   
        else:
            user.financials.address=address
            user.save()
            messages.success(request,"Successfully Added Financial")
            return HttpResponseRedirect(reverse("staff_account"))




def staff_account(request):
    financials=Financials.objects.all()
    adminciis=AdminCIIS.objects.all()
    return render(request,"admin_templates/staff_account.html",{"financials":financials,"adminciis":adminciis})



def approve_payment(request):
    obj_author=Approvalauthor.objects.filter(statusapproval="Waiting for approval")
    obj_paticipant=Approvalpp.objects.filter(statusapproval="Waiting for approval")
    return render(request,"admin_templates/approve_payment.html",{"obj_author":obj_author,"obj_participant":obj_paticipant})

#Button appove_payment 2 status Approve/Disapproval Author
def approval(request,bill_id):
    obj=Approvalauthor.objects.get(billid=bill_id)
    obj.statusapproval="Approve"
    obj.save()
    
    obj2=Paymentpaper.objects.get(bill_id=bill_id)
    obj2.status="Overdue"
    obj2.save()
    
    return redirect('approve_payment')
def disapproval(request,bill_id):
    obj=Approvalauthor.objects.get(billid=bill_id)
    obj.statusapproval="Disapproval"
    obj.save()

    obj2=Paymentpaper.objects.get(bill_id=bill_id)
    obj2.status="Success"
    obj2.save()
    return redirect('approve_payment')


#Button appove_payment 2 status Approve/Disapproval Participant
def approvalpp(request,bill_id):
    obj=Approvalpp.objects.get(billid=bill_id)
    obj.statusapproval="Approve"
    obj.save()
    
    obj2=Memberparticipant.objects.get(id=bill_id)
    obj2.status="Overdue"
    obj2.save()
    
    return redirect('approve_payment')
def disapprovalpp(request,bill_id):
    obj=Approvalpp.objects.get(billid=bill_id)
    obj.statusapproval="Disapproval"
    obj.save()

    obj2=Memberparticipant.objects.get(id=bill_id)
    obj2.status="Success"
    obj2.save()
    return redirect('approve_payment')




def edit_financial(request,financial_id):
    financial=Financials.objects.get(admin=financial_id)
    return render(request,"admin_templates/edit_financial.html",{"financial":financial,"id":financial_id})



    
def edit_financial_save(request,financial_id):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=financial_id)
            financial_model=Financials.objects.get(admin=financial_id)

            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=email
            financial_model.address=address
            try:
                user.save()
                financial_model.save()
            except:
                raise Exception("The email address has been taken.")
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse("edit_financial",kwargs={"financial_id":financial_id}))
        else:
            messages.success(request,"Successfully Edited Financial")
            return redirect("staff_account")

def ban_admin(request,id):
    obj=CustomUser.objects.get(id=id)
    obj.is_active=False
    obj.save()
    return redirect("staff_account")

def export(request):
    dataciis_resource = DataCIISResource()
    dataset = dataciis_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tbl1.xls"'
    return response

def simple_upload(request):
    dataciis=DataCIIS.objects.all()
    if request.method == 'POST':
        dataciis_resource = DataCIISResource()
        dataset = Dataset()
        new_dataciis = request.FILES['myfile']
        
        imported_data = dataset.load(new_dataciis.read(),format='xlsx')
        print(imported_data)
        for data in imported_data:
        	value = DataCIIS(
        		data[0],
        		data[1],
        		 data[2],
        		 data[3],
                 data[4],
                 data[5]
        		)
        	value.save() 
    return render(request, "admin_templates/manages.html",{"dataciis":dataciis})



def edit_dataciis(request,dataciis_id):
    dataciis=DataCIIS.objects.get(id=dataciis_id)
    return render(request,"admin_templates/edit_dataciis.html",{"dataciis":dataciis,"id":dataciis_id})




def edit_dataciis_save(request,dataciis_id):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        paper_id=request.POST.get("paper_id")
        email=request.POST.get("email")
        paper_title=request.POST.get("paper_title")
        paper_type=request.POST.get("paper_type")
        author_name=request.POST.get("author_name")
        try:
            data=DataCIIS.objects.get(id=dataciis_id)
            data.paper_id=paper_id
            data.author_email=email
            data.paper_title=paper_title
            data.author_name=author_name
            data.save()
        
            messages.success(request,"Successfully")
            return HttpResponseRedirect('/manages')
        except:
            messages.error(request,"Failed")
            return HttpResponseRedirect(reverse("edit_dataciis",kwargs={"dataciis_id":dataciis_id}))












def add_author(request):
    return render(request,"admin_templates/add_author.html")
def register_save_admin(request):
     if request.method!="POST":
            return HttpResponse("Method Not Allowed")
     else:
        title=request.POST.get("title")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        phone_number=request.POST.get("phoneNum")
        passport_id=request.POST.get("ppID")
        affiliation=request.POST.get("affiliation")
        country=request.POST.get("contrys")
        nationality=request.POST.get("nationality")
        status=request.POST.get("drone")
        email=request.POST.get("email")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        try:
            if nationality == "thai":
                status = "authorthai"
            elif nationality!= "thai":
                status = "authorforeigner"
            if password != cpassword:
                raise Exception("Password not match")
            try:
                user = CustomUser.objects.create_user(username=email,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            except:
                raise Exception("The email address has been taken.")
        except Exception as e:
            messages.error(request,e)
            return HttpResponseRedirect(reverse("add_author"))
        else:
            user.authors.phoneno=phone_number
            user.authors.passportid=passport_id
            user.authors.affiliation=affiliation
            user.authors.country=country
            user.authors.nationality=nationality
            user.authors.status=status
            user.save()
            messages.success(request,"Successfully Added Author")
            return HttpResponseRedirect(reverse("member_account"))

    
def member_regular(request):
    member=Authors.objects.filter(status="authorthai")
    return render(request,"admin_templates/manage_member_thai.html",{"member":member})


def exhibitors(request):
    regular=Paymentpaper.objects.filter(status="Success" ,author_type="Regular")
    downgrade=Paymentpaper.objects.filter(status="Downgrade")
    virtual=Paymentpaper.objects.filter(status="Success",author_type="Virtual")
    parti=Memberparticipant.objects.filter(status="Success")
    return render(request,"admin_templates/exhibitors.html",{"regular":regular,"virtual":virtual,"downgrade":downgrade,"parti":parti})
    
def member_account(request):
    author=Authors.objects.all()
    participant=Participants.objects.all()
    return render(request,"admin_templates/member_account.html",{"author":author,"participant":participant})
def manage_owners(request):
    paper=paperauthor.objects.all()
    return render(request,"admin_templates/manage_owners.html",{"paper":paper})

def cancel_owners(request, id):
    obj = paperauthor.objects.get(pk = id)
    obj.delete()
    messages.success(request,"Cancel Success")
    return redirect('manage_owners')


def member_downgrade(request):
    member=Paymentpaper.objects.filter(status="Downgrade")
    return render(request,"admin_templates/member_downgrade.html",{"member":member})


def change_status(request):
    obj_authors=Paymentpaper.objects.filter(status="Success")
    obj_participants=Memberparticipant.objects.filter(status="Success")
    return render(request,"admin_templates/change_status.html",{"obj_authors":obj_authors,"obj_participants":obj_participants})



#####CHANGE STATUS BY ADMIN
def change_overdue(request, id):
    obj = Paymentpaper.objects.get(pk = id)
    obj.status="Overdue"
    obj.save()
    messages.success(request,"Cancel Success")
    return redirect('change_status')

