from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', index, name="index"),
   path("about/", about, name="about"),
   path("contact/", contact, name="contact"),
   path("menu/", menu, name="menu"),
   path("services/", services, name="services"),
   path("testemonial/", testemonial, name="testemonial"),


   #auth part
   path("login/", log_in, name='login'),
   path("register/", register, name='register'),
   path("logout/", log_out, name='logout'),
   path("password_change/",password_change, name="password_change"),
   path('password_reset/', auth_views.PasswordResetView.as_view(html_email_template_name='auth/mail.html'), name='password_reset'),
   path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'auth/password_reset_done.html'), name='password_reset_done'),
   path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name= 'auth/password_reset_confirm.html'), name='password_reset_confirm'),
   path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/PasswordResetCompleteView.html'), name='password_reset_complete'),
]
