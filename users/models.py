from django.db import models
from django.contrib.auth.models import AbstractUser
import random
class CustomUser(AbstractUser):
    positions = models.CharField(max_length=100)
    salary = models.FloatField()
    phone_number = models.CharField(max_length=11,unique=True)
    password = models.CharField(max_length=20,null=False)
    hire_date = models.DateField()
    insurance_amount = models.FloatField()
    final_salary = models.FloatField()
    reward = models.FloatField()

class Leave(models.Model) : 
    leave_type_choice =[
        (1 , 'Hourly'),
        (2 , 'Daily')
        ] 
    employee = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    absences = models.IntegerField(default=0) 
    request_text = models.TextField()
    status = models.BooleanField(default=False)
    leave_type = models.CharField(max_length=6, choices=leave_type_choice)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  
    start_time = models.TimeField(null=True, blank=True)  
    end_time = models.TimeField(null=True, blank=True)  
    rejection_comment = models.TextField(null=True , blank=True)
    number_request = models.IntegerField(unique=True)
    username =models.CharField(max_length=255) 

class Letter(models.Model) : 
    subject = models.CharField(max_length=255)
    text = models.TextField()
    letter_number = models.IntegerField(unique=True , blank=True , null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_letters', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_letters', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.letter_number:
            self.letter_number = self.generate_unique_letter_number()
        super().save(*args, **kwargs)

    def generate_unique_letter_number(self):
        while True:
            number = random.randint(1, 999999)
            if not Letter.objects.filter(letter_number=number).exists():
                return number

