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
    path('token/verify', TokenVerifyView.as_view()),
    # 获取单个用户信息的路由
    path('user/<int:pk>', views.UserView.as_view({'get': 'retrieve'})),
    # 上传用户头像的路由
    path('<int:pk>/avatar/upload', views.UserView.as_view({
        "post": "upload_avatar"
    })),
    # 添加地址和获取地址列表的路由
    path('user/address', views.AddrView.as_view({
        "post": "create",
        "get": "list"
    }))
]
