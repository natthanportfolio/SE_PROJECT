"""ciis_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ciis_system import settings
from django.conf.urls.static import static
from ciis_app import AdminViews, FinancialViews, views ,participantViews, authorViews, authorFViews
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from ciis_app.views import CompletePasswordReset, RequestPasswordResetEmail,VerificationView


urlpatterns = [
  
    path('',views.showLoginPage,name="show_login"),

    path('get_user_details', views.GetUserDetails),
    path('doLogin',views.doLogin,name="do_login"),


    path('register',views.doRegister,name="doRegister"),
    path('register_save',views.register_save,name="register_save"),

    path('activate/<uidb64>/<token>',VerificationView.as_view(),name="activate"),
    path('set-new-password/<uidb64>/<token>',CompletePasswordReset.as_view(),name="reset-user-password"),
    path('request-reset-link',RequestPasswordResetEmail.as_view(),name="request-password"),

    



#Admin
    #SuperAdmin
    path('add_author',AdminViews.add_author,name="add_author"),
    path('member_account',AdminViews.member_account,name="member_account"),
    path('exhibitors',AdminViews.exhibitors,name="exhibitors"),
    path('manage_owners',AdminViews.manage_owners,name="manage_owners"),
    path('cancel_owners/<str:id>',AdminViews.cancel_owners,name="cancel_owners"),

    path('member_downgrade',AdminViews.member_downgrade),
    path('register_save_admin',AdminViews.register_save_admin,name="register_save_admin"),
    

    path('manages',AdminViews.simple_upload,name="manages"),
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('add_financial',AdminViews.add_financial,name="add_financial"),
    path('add_financial_save',AdminViews.add_financial_save,name="add_financial_save"),
    path('add_admin',AdminViews.add_admin,name="add_admin"),
    path('add_admin_save',AdminViews.add_admin_save,name="add_admin_save"),
    path('staff_account',AdminViews.staff_account,name="staff_account"),
    path('approve_payment',AdminViews.approve_payment,name="approve_payment"),
    path('approval/<str:bill_id>',AdminViews.approval,name="approval"),
    path('disapproval/<str:bill_id>',AdminViews.disapproval,name="disapproval"),
    path('approvalpp/<str:bill_id>',AdminViews.approvalpp,name="approvalpp"),
    path('disapprovalpp/<str:bill_id>',AdminViews.disapprovalpp,name="disapprovalpp"),
    path('change_status',AdminViews.change_status,name="change_status"),
    path('change_overdue/<str:id>',AdminViews.change_overdue,name="change_overdue"),

    path('ban_admin/<str:id>',AdminViews.ban_admin,name="ban_admin"),


    path('edit_financial/<str:financial_id>',AdminViews.edit_financial,name="edit_financial"),
    path('edit_financial_save/<str:financial_id>', AdminViews.edit_financial_save,name="edit_financial_save"),
    path('edit_dataciis/<str:dataciis_id>',AdminViews.edit_dataciis,name="edit_dataciis"),
    path('edit_dataciis_save/<str:dataciis_id>', AdminViews.edit_dataciis_save,name="edit_dataciis_save"),

    #exportExcel

    url('export/csv/', AdminViews.export_users_csv, name='export_users_csv'),
    
    #Financial
    path('financial_home',FinancialViews.financial_home,name="financial_home"),
    path('financial_approval_history_author',FinancialViews.financial_approval_history_author,name="financial_approval_history_author"),
    path('financial_approval_history_Participant',FinancialViews.financial_approval_history_Participant,name="financial_approval_history_Participant"),

    path('financial_payment_update_author',FinancialViews.financial_payment_update_author,name="financial_payment_update_author"),
    path('cancel_statusat/<str:id>',FinancialViews.cancel_statusat,name="cancel_statusat"),
    path('success_statusat/<str:id>',FinancialViews.success_statusat,name="success_statusat"),

    
    path('financial_payment_update_Participant',FinancialViews.financial_payment_update_Participant,name="financial_payment_update_Participant"),
    path('cancel_statuspp/<str:id>',FinancialViews.cancel_statuspp,name="cancel_statuspp"),
    path('success_statuspp/<str:id>',FinancialViews.success_statuspp,name="success_statuspp"),
    

    path('financial_status_change_request_author',FinancialViews.financial_status_change_request_author,name="financial_status_change_request_author"),
    path('change_statusat/<str:id>',FinancialViews.change_statusat,name="change_statusat"),

    path('financial_status_change_request_Participant',FinancialViews.financial_status_change_request_Participant,name="financial_status_change_request_Participant"),
    path('change_statuspp/<str:id>',FinancialViews.change_statuspp,name="change_statuspp"),

#Client
    #Authorthai
    path('author_home',authorViews.author_home,name="author_home"),
    path('author_add_paperid',authorViews.author_add_paperid,name="author_add_paperid"),
    path('author_addpaperid_save',authorViews.author_addpaperid_save,name="author_addpaperid_save"),

    path('author_payment_history',authorViews.author_payment_history,name="author_payment_history"),
    path('author_choose_paper',authorViews.author_choose_paper,name="author_choose_paper"),

    path('author_bill',authorViews.author_bill,name="author_bill"),
    path('author_bill_save/<str:paper_id>',authorViews.author_bill_save,name="author_bill_save"),

    path('author_upload_payment',authorViews.author_upload_payment,name="author_upload_payment"),
    path('update-profile-image/<str:bill_id>',authorViews.update_profile_image,name="update_profile_image"),

    path('author_change_status',authorViews.author_change_status,name="author_change_status"),
    path('author_change_status_save/<str:bill_id>',authorViews.author_change_status_save,name="author_change_status_save"),

    path('author_edit',authorViews.author_edit,name="author_edit"),
    path('author_edit_save',authorViews.author_edit_save,name="author_edit_save"),

###################################################################3
    path('<int:pk>',authorViews.PDFUserDetailView.as_view()),

###############
    path('<int:pk>/<str:banquet>',participantViews.PDFUserDetailView.as_view(),),
 #######################################################################33

    #Authorforeigner
    path('authorf_home',authorFViews.authorf_home,name="authorf_home"),

    path('authorf_add_paperid',authorFViews.authorf_add_paperid,name="authorf_add_paperid"),
    path('authorf_addpaperid_save',authorFViews.authorf_addpaperid_save,name="authorf_addpaperid_save"),

    path('authorf_payment_history',authorFViews.authorf_payment_history,name="authorf_payment_history"),
    
    path('authorf_choose_paper',authorFViews.authorf_choose_paper,name="authorf_choose_paper"),
    path('authorf_bill_save/<str:paper_id>',authorFViews.authorf_bill_save,name="authorf_bill_save"),

    path('authorf_upload_payment',authorFViews.authorf_upload_payment,name="authorf_upload_payment"),

    path('authorf_edit',authorFViews.authorf_edit,name="authorf_edit"),
    path('authorf_edit_save',authorFViews.authorf_edit_save,name="authorf_edit_save"),

    path('checkout/<int:pk>/', authorFViews.checkout, name="checkout"),
    path('complete/', authorFViews.paymentComplete, name="complete"),



    #Participant
    path('participant_home',participantViews.participant_home,name="participant_home"),
    path('participant_payment_history',participantViews.participant_payment_history,name="participant_payment_history"),
    path('participant_payment',participantViews.participant_payment,name="participant_payment"),
    
    path('participant_edit',participantViews.participant_edit,name="participant_edit"),

    path('participant_edit',participantViews.participant_edit,name="participant_edit"),
    path('participant_edit_save',participantViews.participant_edit_save,name="participant_edit_save"),

    path('new',participantViews.new,name="new"),
    path('new_save',participantViews.new_save,name="new_save"),
    
    path('participant_payment_2',participantViews.participant_payment_2,name="participant_payment_2"),
    
    path('participant_payment_save',participantViews.participant_payment_save,name="participant_payment_save"),

    path('participant_upload_payment',participantViews.participant_upload_payment,name="participant_upload_payment"),
    path('update_profile_images/<str:id>',participantViews.update_profile_images,name="update_profile_images"),




    path('Logout',views.Logout,name="Logout"),


]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
