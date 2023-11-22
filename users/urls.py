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
    # 添加收货地址和获取收货地址列表的路由
    path('address', views.AddrView.as_view({
        "post": "create",
        "get": "list"
    })),
    # 修改收货地址和删除时候地址的路由
    path('address/<int:pk>', views.AddrView.as_view({
        "delete": "destroy",
        "put": "update"
    })),
    # 设置默认收货地址
    path('address/<int:pk>/default', views.AddrView.as_view({
        "put": "set_default_addr",
    }))
]
