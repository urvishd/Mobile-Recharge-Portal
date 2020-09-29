from django.db import models
from django import forms
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Transactions(models.Model):
    Transactions_ID = models.AutoField(primary_key=True)
    User_mobile = models.CharField(max_length=10)
    Recharge_mobile = models.CharField(max_length=10)
    Operator = models.CharField(max_length=10)
    Amount = models.CharField(max_length=5)
    Status = models.CharField(default="Failed", max_length=15)
    Payment_method = models.CharField(blank=True, max_length=15)
    Date_Time = models.CharField(default=timezone.now(), max_length=19)


class Cards(models.Model):
    Card_number = models.CharField(primary_key=True, max_length=16)
    Ex_month = models.CharField(max_length=2)
    Ex_Year = models.CharField(max_length=2)
    CVV = models.CharField(max_length=3)
    Balance = models.CharField(max_length=5)
    email=models.EmailField(max_length=50,default='devaniurvish881@gmail.com')

class Plans(models.Model):
    Operator=models.CharField(max_length=20)
    Amount=models.IntegerField()
    Talktime=models.IntegerField()
    Description=models.CharField(max_length=200)
    Validity=models.CharField(max_length=25)


class NetBanking(models.Model):
    Username = models.CharField(primary_key=True, max_length=16)
    Password = models.CharField(max_length=14)
    Bank=models.CharField(max_length=25)
    Balance = models.CharField(max_length=5)

class Plans(models.Model):
    Operator=models.CharField(max_length=15)
    Price=models.IntegerField()
    Talktime=models.FloatField()
    Benifits=models.CharField(max_length=200)
    validity=models.CharField(max_length=25)
