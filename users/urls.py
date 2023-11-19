from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users import views

urlpatterns = [
    # 登录
    path('login', views.LoginView.as_view()),
    # 注册
    path('register', views.RegisterView.as_view()),
    # 刷新token
    path('token/refresh', TokenRefreshView.as_view()),
    # 校验token
    path('token/verify', TokenVerifyView.as_view())
]
