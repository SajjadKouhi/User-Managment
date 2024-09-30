from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from users.models import CustomUser , Leave , Letter
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class UserRegisterByAdminView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, kwargs):
        return Response(status=status.HTTP_200_OK)

class UserEditByAdminView(generics.RetrieveUpdateDestroyAPIView) :
    queryset = CustomUser.objects.all()
    serializer_class = UserEditSerializers
    permission_classes = [permissions.IsAdminUser]

class UserListView(generics.ListAPIView) : 
    queryset = CustomUser.objects.all()
    serializer_class = ListUserSerializer
    permission_classes = [permissions.IsAdminUser]

class StatusLeaveView(generics.RetrieveUpdateAPIView) :
    serializer_class = LeaveCheckSerializer
    permission_classes = [permissions.IsAdminUser]
    def get_queryset(self):
        user = self.request.user
        leavs = Leave.objects.filter(employee = user)
        return  leavs
    def get_object(self):
        queryset = self.get_queryset()
        number_request = self.kwargs.get('number_request')
        obj = get_object_or_404(queryset , number_request=number_request)
        return obj
class LeaveListView(generics.ListAPIView) : 
    queryset = Leave.objects.all()
    serializer_class = LeaveDetailShowSerializer
    permission_classes = [permissions.IsAdminUser]    


class RegisterLetterView(generics.CreateAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterRegisterSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
class ShowLetterView(generics.ListAPIView) : 
    permission_classes = [IsAdminUser]
    serializer_class = ShowLetterSerializer
    queryset = Letter.objects.all()

class ShowLetterSenderView(generics.ListAPIView) :
       permission_classes = [IsAdminUser]
       serializer_class = ShowLetterSerializer
       def get_queryset(self):
           user = self.request.user
           letter = Letter.objects.filter(sender = user)
           return letter       

class ShowLetterRecipientView(generics.ListAPIView) :
       permission_classes = [IsAdminUser]
       serializer_class = ShowLetterSerializer
       def get_queryset(self):
           user = self.request.user
           letter = Letter.objects.filter(recipient = user)
           return letter