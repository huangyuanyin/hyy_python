import re

from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from users.models import User


class RegisterView(APIView):
    def post(self, request):
        """用户注册"""
        # 1. 接收用户参数
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')

        # 2. 参数校验
        # 2.1 校验参数是否为空
        if not all([username, email, password, password_confirmation]):
            return Response({'error': "所有参数不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2.2 校验用户名是否为空
        if User.objects.filter(username=username).exists():
            return Response({'error': "用户名已存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2.3 校验两次密码是否一致
        if password != password_confirmation:
            return Response({'error': "两次密码不一致"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2.4 校验密码长度
        if not (6 <= len(password) <= 18):
            return Response({'error': "密码长度需要在6到18位之间"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2.5 校验邮箱是否存在
        if User.objects.filter(email=email).exists():
            return Response({'error': "该邮箱已被其他用户使用"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 2.6 校验邮箱格式是否正确
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': "邮箱格式有误！"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # 3. 创建用户
        obj = User.objects.create_user(username=username, email=email, password=password)
        res = {
            'username': username,
            'id': obj.id,
            'email': obj.email
        }
        return Response(res, status=status.HTTP_201_CREATED)


# Create your views here.
class LoginView(TokenObtainPairView):
    """"用户登录"""
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        # 自定义登录成功之后返回的结果
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
