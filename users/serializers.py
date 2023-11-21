from rest_framework import serializers
from users.models import User, Addr


class UserSerializer(serializers.ModelSerializer):
    """"用户模型的序列化器"""
    class Meta:
        model = User
        # fields = '__all__'  # 返回所有
        fields = ['id', 'username', 'mobile', 'email', 'avatar', 'last_name']


class AddrSerializer(serializers.ModelSerializer):
    """收货地址模型的序列号器"""
    class Meta:
        model = Addr
        fields = '__all__'
