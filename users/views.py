import os
import re

from django.http import FileResponse
from django.shortcuts import render
from rest_framework import status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from hyy_python.settings import MEDIA_ROOT
from users.models import User
from .permissions import UserPermissions
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


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


class UserView(GenericViewSet, mixins.RetrieveModelMixin):
    """用户相关操作的视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 设置认证用户才能有权限访问
    permission_classes = [IsAuthenticated, UserPermissions]

    def upload_avatar(self, request, *arg, **kwargs):
        """"上传用户头像"""
        avatar = request.data.get('avatar')
        # 校验是否有上传文件
        if not avatar:
            return Response({'error': '上传失败，文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 校验文件大小不能超过300kb
        if avatar.size > 1024 * 300:
            return Response({'error': '上传失败，文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # 保存文件
        user = self.get_object()
        # 获取序列号对象
        ser = self.get_serializer(user, data={"avatar": avatar}, partial=True)
        # 校验
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({'url': ser.data['avatar']})


class FileView(APIView):
    """获取文件的视图"""
    def get(self, request, name):
        path = MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': "没有找到该文件！"}, status=status.HTTP_404_NOT_FOUND)
