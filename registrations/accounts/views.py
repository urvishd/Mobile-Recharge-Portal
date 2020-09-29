from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import *
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.views.decorators.cache import cache_control
from accounts.models import Transactions
from accounts.models import Cards
from django.core.mail import send_mail
import random
from accounts.models import NetBanking
from accounts.models import Plans
from django.contrib.auth.hashers import make_password


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User already exists!!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already linked with other account')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                fname = first_name
                mail = email
                ctx = {
                    'fname': fname
                }
                message = get_template('login_alert.html').render(ctx)
                msg = send_mail('Welcome to Freecharge',
                                message,
                                'freerechargepaymentsltd@gmail.com',
                                [mail],
                                fail_silently=False, html_message=message)
        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')
        messages.info(request, 'You have successfully signed up!!')
        return render(request, 'login.html')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        request.session['passwd']=password

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            request.session['mailid'] = user.email
            request.session['user_name'] = username
            return redirect('homepage')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out!!')
    return render(request, 'login.html')


@login_required(login_url='/accounts/login')
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def homepage(request):
    request.session['status']='failed'
    return render(request, 'home.html')


def view_plan(request):
    pass


@login_required(login_url='/accounts/login')
def payment_page(request):
    if request.method == 'POST' and 'Plan_button' in request.POST:
        operator = request.POST['Operator']
        plan_data = Plans.objects.filter(Operator=operator)
        stu = {
            "plan_data": plan_data
        }
        return render(request,'Plans.html',stu)
    else:
        mobile = request.POST['mobile']
        operator = request.POST['Operator']
        amount = request.POST['amount']
        user_mobile1 = request.session['user_name']
        request.session["mobile_no"] = mobile
        request.session["pay_amount"] = amount
        request.session['Operator'] = operator
        t = Transactions(User_mobile=user_mobile1, Recharge_mobile=mobile, Operator=operator, Amount=amount)
        t.save()
        request.session['tid'] = t.Transactions_ID
        return render(request, 'payment.html', {'amount': request.session["pay_amount"]})



@login_required(login_url='/accounts/login')
def do_payment(request):
    if request.session['status']=='success':
        return redirect(homepage)
    method = request.POST['pay']
    if method == 'cards':
        amount1 = request.session["pay_amount"]
        return render(request, 'Card.html', {'amount1': amount1})
    else:
        return render(request, 'Netbanking.html')


@login_required(login_url='/accounts/login')
def card_payment(request):
    card_no = request.POST['cardNumber']
    MM = request.POST['expiryMonth']
    YY = request.POST['expiryYear']
    CVV = request.POST['cvCode']
    request.session['dcard'] = card_no
    tr = Transactions.objects.get(Transactions_ID=request.session['tid'])
    tr.Payment_method = 'Debit Card'
    tr.save(update_fields=['Payment_method'])
    tr.save()
    try:
        balance = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).Balance
        request.session['total_balance'] = balance
        mail1 = Cards.objects.get(Card_number=card_no, Ex_month=MM, Ex_Year=YY, CVV=CVV).email
        if int(balance) >= int(request.session['pay_amount']):
            rno = random.randint(100000, 999999)
            request.session['OTP'] = rno
            username = request.session['user_name']
            amt = request.session["pay_amount"]
            mail_id = mail1
            msg = 'Your OTP For Payment of ₹' + amt + ' is ' + str(rno)
            send_mail('OTP for Debit card Payment',
                      msg,
                      'freerechargepaymentsltd@gmail.com',
                      [mail_id],
                      fail_silently=False)
            return render(request, 'OTP.html')
        messages.info(request,'Payment failed due to insufficient Balance.Your Transaction id is ')
        return render(request,'payment.html',{'amount': request.session["pay_amount"],'Tid':request.session['tid']})
    except:
        messages.info(request,'Payment failed due to Invalid Debit Card details.Your Transaction id is ')
        return render(request,'payment.html',{'amount': request.session["pay_amount"],'Tid':request.session['tid']})


@login_required(login_url='/accounts/login')
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def net_payment(request):
    username = request.POST['username']
    Password = request.POST['pass']
    Bank_name = request.POST['banks']
    tr2 = Transactions.objects.get(Transactions_ID=request.session['tid'])
    tr2.Payment_method = 'Net Banking'
    tr2.save(update_fields=['Payment_method'])
    tr2.save()
    try:
        net_obj = NetBanking.objects.get(Username=username, Password=Password, Bank=Bank_name)
        balance1 = net_obj.Balance
        request.session['total_balance1'] = balance1
        if int(balance1) >= int(request.session['pay_amount']):
            rem_balance1 = int(balance1) - int(request.session["pay_amount"])
            net_obj.Balance = rem_balance1
            net_obj.save(update_fields=['Balance'])
            net_obj.save()
            tr3 = Transactions.objects.get(Transactions_ID=request.session['tid'])
            tr3.Status = 'Success'
            tr3.save(update_fields=['Status'])
            tr3.save()
            return redirect('recharge_success')
        messages.info(request, 'Payment failed due to insufficient Balance.Your Transaction id is ')
        return render(request, 'payment.html', {'amount': request.session["pay_amount"],'Tid':request.session['tid']})
    except:
        messages.info(request, 'Payment failed due to Invalid Username or Password.Your Transaction id is ')
        return render(request, 'payment.html', {'amount': request.session["pay_amount"],'Tid':request.session['tid']})


@login_required(login_url='/accounts/login')
def otp_verification(request):
    otp1 = int(request.POST['otp'])
    if otp1 == int(request.session['OTP']):
        del request.session["OTP"]
        total_balance = int(request.session['total_balance'])
        rem_balance = int(total_balance - int(request.session["pay_amount"]))
        c = Cards.objects.get(Card_number=request.session['dcard'])
        c.Balance = rem_balance
        c.save(update_fields=['Balance'])
        c.save()
        tr1 = Transactions.objects.get(User_mobile=request.session['user_name'],
                                       Recharge_mobile=request.session['mobile_no'],
                                       Operator=request.session['Operator'], Amount=request.session['pay_amount'])
        tr1.Status = 'Success'
        tr1.save(update_fields=['Status'])
        tr1.save()
        return redirect(recharge_success)
    else:
        messages.info(request, 'Payment declined by bank due to Wrong OTP.Your Transaction id is ')
        return render(request, 'payment.html', {'amount': request.session["pay_amount"], 'Tid': request.session['tid']})


def forgot_password(request):
    username = request.POST['user_name']
    request.session['forgot_user'] = username
    try:
        user = User.objects.get(username=username)
        email_id = user.email
        rno1 = random.randint(100000, 999999)
        request.session['OTP1'] = rno1
        msg = 'Your OTP For Password Reset is ' + str(rno1)
        send_mail('OTP for Password Reset',
                  msg,
                  'freerechargepaymentsltd@gmail.com',
                  [email_id],
                  fail_silently=False)
        return render(request, 'forgot_otp.html')
    except User.DoesNotExist:
        messages.info(request, 'Invalid Username')
        return render(request, 'forgot_password.html')


def otp_verification1(request):
    otp1 = int(request.POST['otp1'])
    if otp1 == int(request.session['OTP1']):
        del request.session["OTP1"]
        # user = User.objects.get(username= request.session['forgot_user'])
        return render(request, 'set_password.html')
    else:
        messages.info(request, 'OTP verification Failed:(')
        return render(request, 'forgot_otp.html')


def set_passwords(request):
    new_pass = request.POST['pass2']
    user = User.objects.get(username=request.session['forgot_user'])
    user.password = make_password(new_pass)
    user.save(update_fields=['password'])
    user.save()
    messages.info(request, 'Password successfully reseted!!')
    return render(request, 'login.html')


def user_forgot(request):
    return render(request, 'forgot_password.html')


@login_required(login_url='/accounts/login')
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def recharge_success(request):
    if request.session['status']=='success':
        return redirect(homepage)
    request.session['status']='success'
    user_mobile = request.session['user_name']
    recharge_mobile = request.session["mobile_no"]
    amount = request.session["pay_amount"]
    operator = request.session['Operator']
    mail_id = request.session['mailid']
    u=User.objects.get(username=user_mobile)
    fname=u.first_name
    tid = request.session['tid']
    ctx = {
        'fname': fname,
        'recharge_mobile': recharge_mobile,
        'amount': amount,
        'tid': tid
    }
    message = get_template('success_message.html').render(ctx)
    msg = send_mail('Recharge Successful!!',
                   message,
                    'freerechargepaymentsltd@gmail.com',
                    [mail_id],
                    fail_silently=False, html_message=message)
    return render(request, 'Final_page.html',{'Tid':request.session['tid'],'Mobile':request.session['mobile_no'],'Operator':request.session['Operator'],'Amt':request.session['pay_amount']})


@login_required(login_url='/accounts/login')
def Payment_abort(request):
    del request.session['mobile_no']
    del request.session['pay_amount']
    del request.session['Operator']
    return render(request,'home.html')


def transactions(request):
    transaction_data = Transactions.objects.filter(User_mobile=request.session['user_name'])
    if transaction_data.exists():
        stu = {
            "transaction_data": transaction_data
        }
        return render(request,'Transactions.html',stu)
    else:
        return render(request,'no_transaction.html')

@login_required(login_url='/accounts/login')
def profile_view(request):
    return render(request,'profile.html')

@login_required(login_url='/accounts/login')
def change_pass(request):
    pass1=request.POST['pass1']
    pass2 = request.POST['pass2']
    pass3 = request.POST['pass3']
    user = User.objects.get(username=request.session['user_name'])
    passwd=request.session['passwd']
    if pass2==pass3:
        if passwd==pass1:
            user.password = make_password(pass2)
            user.save(update_fields=['password'])
            user.save()
            messages.info(request,'Password changed successfully:)')
        else:
            messages.info(request, 'Please enter right password!!')
    else:
        messages.info(request, 'Confirmed Password not matching!!')
    return render(request,'profile.html')

def index_page(request):
    return render(request,'login.html')