from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^homepage/$',views.homepage,name='homepage'),
    url(r'^payment_page/$',views.payment_page, name='payment_page'),
    url(r'^do_payment/$',views.do_payment, name='do_payment'),
    url(r'^card_payment/$',views.card_payment, name='card_payment'),
    url(r'^net_payment/$',views.net_payment, name='net_payment'),
    url(r'^otp_verification/$',views.otp_verification, name='otp_verification'),
    url(r'^forgot_password/$',views.forgot_password, name='forgot_password'),
    url(r'^otp_verification1/$',views.otp_verification1, name='otp_verification1'),
    url(r'^set_passwords/$',views.set_passwords, name='set_passwords'),
    url(r'^user_forgot/$',views.user_forgot, name='user_forgot'),
    url(r'^recharge_success/$', views.recharge_success, name='recharge_success'),
    url(r'^view_plan/$', views.view_plan, name='view_plan'),
    url(r'^Payment_abort/$', views.Payment_abort, name='Payment_abort'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^profile_view/$', views.profile_view, name='profile_view'),
    url(r'^change_pass/$', views.change_pass, name='change_pass'),
    url(r'^index_page/$', views.index_page, name='index_page'),
]
