from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/' , LogoutView.as_view() , name = 'user_logout'),
    path('forgetpassword/' , ForgetPasswordView.as_view() , name = 'forget_password'),
    path('userdetail/' , ShowUserDetailView.as_view() , name = 'user_detail_show') , 
    path('resetPassword/' , ResetPasswordView.as_view() , name= 'reset_password'),
    path('requestleave/' , LeaveRequestView.as_view() , name = 'requset_leave') , 
    path('detailLeave/' , LeaveRequestDetailView.as_view() , name='detail_leave') , 
    path('editleave/<int:number_request>/' , EditLeaveView.as_view() , name= 'edit_leave'),
    path('payslip/' , ShowPayslipView.as_view() , name = 'payslip_show') , 
    path('showlettersender/' , ShowLetterSenderView.as_view() , name = 'show_letter_user_sender'),
    path('registerletter/', RegisterLetterView.as_view() , name='register_letter'),
    path('showletterrecipient/' , ShowLetterRecipientView.as_view() , name = 'show_letter_user_recipient'),
]
