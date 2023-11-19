from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """"用户模型的序列化器"""
    class Meta:
        model = User
        # fields = '__all__'  # 返回所有
        fields = ['id', 'username', 'mobile', 'email', 'avatar', 'last_name']
