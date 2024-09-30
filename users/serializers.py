import attrs
from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from . models import CustomUser , Leave , Letter
import uuid
from datetime import date


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email' , 'phone_number' , 'salary' ,  'first_name' , 'last_name' , 'positions' , 'hire_date','insurance_amount'  , 'reward')

    def create(self, validated_data):
        username_random = str(randint(1000 , 9999))
        password_random = str(randint(10000 , 99999))
        user = User(
            password = password_random,
            username=username_random ,  
            email=validated_data['email'],
            phone_number = validated_data['phone_number'],
            salary = validated_data['salary'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'], 
            positions = validated_data['positions'],
            hire_date = validated_data['hire_date'],
            insurance_amount = validated_data['insurance_amount'],
            reward = validated_data['reward'],
            final_salary = (validated_data['salary'] - validated_data['insurance_amount'])+validated_data['reward'],
            is_staff = True,
            is_superuser = True
        )
        user.set_password(password_random)  
        user.save()
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': username_random, 
            'password': password_random,  
            'salary': user.salary,
            'positions': user.positions,
            'hire_date' : user.hire_date
        }
class UserEditSerializers(serializers.ModelSerializer) : 
    class Meta : 
        model = User
        fields = ('phone_number' , 'salary' , 'first_name' , 'last_name')
  
class LoginUserSerializer(serializers.Serializer):
    class Meta : 
        model  = User
        fields = ['username' , 'password']

class ListUserSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = User
        fields = [ 'id', 'username' , 'salary' , 'first_name' , 'last_name' , 'positions' , 'hire_date']

class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return data

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance
    
class ShowUserDetailSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = User
        fields = ['username' , 'salary' , 'first_name' , 'last_name' , 'positions' , 'hire_date']

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user 

        if not user.check_password(data['password']):
            raise serializers.ValidationError('PASSWORD IS INCORRECT!!.')

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("NEW PASSWORD AND CONFIRM PASSWORD DO NOT MATCH.")

        return data

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        instance.set_password(new_password)
        instance.save()
        return instance     
       

class RequestLeaveSerializer(serializers.ModelSerializer):
    number_request = serializers.IntegerField(read_only = True)
    username = serializers.CharField(read_only = True)
    class Meta:
        model = Leave
        fields = ['id','username', 'leave_type', 'start_date', 'end_date', 'start_time', 'end_time', 'request_text' , 'number_request']

    def get_employee(self , obj) :
        
        return obj.employee.first_name
        
    def validate(self, data):
        if data['leave_type'] == '1':  # Hourly
            if not data.get('start_time') or not data.get('end_time'):
                raise serializers.ValidationError("START TIME AND END TIME ARE REQUIRED FOR HOURLY LEAVE.")
            if data['start_time'] >= data['end_time']:
                raise serializers.ValidationError("END TIME MUST BE AFTER START TIME.")
        elif data['leave_type'] == '2':  # Daily
            if not data.get('end_date'):
                raise serializers.ValidationError("END DATE IS REQUIRED FOR DAILY LEAVE.")
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("END DATE MUST BE AFTER START DATE.")
        
        return data

    def create(self, validated_data):
        number_request_random = randint(100000,9999999)
        number_request = number_request_random
        request = self.context.get('request', None)
        if request is None:
            raise serializers.ValidationError("Request context is missing.")
        
        user = request.user
        if 'user' in validated_data:
            validated_data.pop('user')

        leave_request = Leave.objects.create(employee=user, number_request=number_request ,username = user.get_full_name(),**validated_data)
        return leave_request

class LeaveCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['id', 'employee', 'leave_type', 'start_date', 'end_date', 'start_time', 'end_time', 'status', 'rejection_comment']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.rejection_comment = validated_data.get('rejection_comment', instance.rejection_comment)
        instance.save()
        return instance    
    
class LeaveDetailShowSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = Leave
        fields = '__all__'    
class EditLeaveSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = Leave
        fields = ['start_date' , 'end_date' , 'start_time' , 'end_time']        
class PayslipSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = User
        fields = [ 'first_name','last_name', 'insurance_amount' , 'final_salary' , 'reward' , 'salary']
class LetterRegisterSerializer(serializers.ModelSerializer):
    recipient = serializers.SlugRelatedField(queryset = User.objects.all() , slug_field = 'username')
    class Meta:
        model = Letter
        fields = ['id', 'subject', 'text', 'sender', 'recipient', 'sent_at','letter_number']
        read_only_fields = ['sender', 'sent_at']
        
class ShowLetterSerializer(serializers.ModelSerializer) : 
    class Meta : 
        model = Letter
        fields = ['subject', 'text', 'sender', 'recipient', 'sent_at' , 'letter_number']
