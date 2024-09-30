from django.urls import path
from .views import *
urlpatterns = [
    path('registeruser/', UserRegisterByAdminView.as_view(), name='user-register'),
    path('edituser/<int:pk>/' , UserEditByAdminView.as_view() , name='user_edit'),
    path('listuser/' , UserListView.as_view() , name='list_user') , 
    path('editleave/<int:pk>/' , StatusLeaveView.as_view() , name = 'status_edit_leave'),
    path('registerletter/', RegisterLetterView.as_view() , name='register_letter'),
    path('showletter/',ShowLetterView.as_view(), name='show_letter_detail') , 
    path('showletterrecipient/' , ShowLetterRecipientView.as_view() , name = 'show_letter_user_recipient'),
    path('showlettersender/' , ShowLetterSenderView.as_view() , name = 'show_letter_user_sender'),

    
]
