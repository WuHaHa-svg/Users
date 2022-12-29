from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


# 注册
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    # 数据简单校验
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    # 创建用户
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# 登入
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    # 成功后返回token
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    # 校验是否成功
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed('账户信息错误')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('此账户无效')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

    class Meta:
        model = User
        fields = ['password', 'username', 'tokens']


# 注销（此处是让用户无法继续刷新token来实现阻止用户登录）
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()  # 将获取token的请求加入黑名单
        except TokenError:
            self.fail('bad_token')


class UpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['password']


class DelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
