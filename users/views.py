from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import CustomUser
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken ,AccessToken
from rest_framework import permissions


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request,):
        username = request.data.get('username')
        password = request.data.get('password')
        user: CustomUser = CustomUser.objects.filter(username__iexact=username).first()
        if user is not None:
           if user.check_password (password) :   
                login(request, user)
                access = AccessToken.for_user(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(access),
                    'user': user.first_name + user.last_name,
                    'positions': user.positions,
                }, status=status.HTTP_202_ACCEPTED)
           else : 
               return Response('Error! : INCORRECT PASSWORD!!' , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Error! Incorrect credentials', status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView) : 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(phone_number=serializer.validated_data['phone_number'])
                serializer.update(user, serializer.validated_data)
                return Response({"message": "Password has been updated."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowUserDetailView(generics.RetrieveAPIView) : 
    serializer_class = ShowUserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class ResetPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user  
            serializer.update(user, serializer.validated_data)
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class LeaveRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        leave_requests = Leave.objects.filter(user=request.user , context={'request': request})
        serializer = RequestLeaveSerializer(leave_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RequestLeaveSerializer(data=request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
class LeaveRequestDetailView(generics.ListAPIView):
    serializer_class = LeaveDetailShowSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        leavs = Leave.objects.filter(employee = user)
        return  leavs

class EditLeaveView(generics.RetrieveUpdateDestroyAPIView) :
    serializer_class = EditLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        leavs = Leave.objects.filter(employee = user)
        return  leavs
    def get_object(self):
        queryset = self.get_queryset()
        number_request = self.kwargs.get('number_request')
        obj = get_object_or_404(queryset , number_request=number_request)
        return obj
    
class ShowPayslipView (APIView) : 
    # serializer_class = PayslipSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def get_object(self):
    #     return self.request.user
    def get(self , request) :
        user = request.user
        serializer= PayslipSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)

class RegisterLetterView(generics.CreateAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class ShowLettersenderView(generics.ListAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ShowLetterSerializer
       def get_queryset(self):
           user = self.request.user
           letter = Letter.objects.filter(sender = user)
           return letter
class ShowLetterSenderView(generics.ListAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ShowLetterSerializer
       def get_queryset(self):
           user = self.request.user
           letter = Letter.objects.filter(sender = user)
           return letter       

class ShowLetterRecipientView(generics.ListAPIView) :
       permission_classes = [permissions.IsAuthenticated]
       serializer_class = ShowLetterSerializer
       def get_queryset(self):
           user = self.request.user
           letter = Letter.objects.filter(recipient = user)
           return letter