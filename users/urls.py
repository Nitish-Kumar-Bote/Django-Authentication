from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,LoginView,UserView,ForgotPass,Otp_sent,Otp_varify,whatsapp,sms,ChallengesCreateAPIView, BlogPostAPI,ChallengesFilterAPIView,BlogFilterAPIView, ProductsRegister, prodFilterAPIView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    # path('sendotp/',RandomView.as_view()),
    path('forgotpass/',ForgotPass.as_view()),
    path('sentotp/',Otp_sent.as_view()),
    path('verify/',Otp_varify.as_view()),
    path('whatsappotp/',whatsapp.as_view()),
    path('sms/',sms.as_view()),
    path('challengespost/', ChallengesCreateAPIView.as_view()),
    path('challengespost/<str:stack>/<str:level>/', ChallengesFilterAPIView.as_view(), name='challenges-filter'),
    path('blog/', BlogPostAPI.as_view()),
    path('blog/<str:title>/', BlogFilterAPIView.as_view(), name='challenges-filter'),
    path('Productregister/', ProductsRegister.as_view()),
    path('Productregister/<str:productname>/', prodFilterAPIView.as_view(), name='filter'),
]






