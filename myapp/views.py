from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, UpdateSerializer, DelSerializer
from .models import User
import base64
import json
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

# 注册视图
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


# 登录视图
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 注销视图
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 删除账户
class DeleteAccountAPIView(generics.GenericAPIView):
    serializer_class = DelSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        try:
            auth_token = request.META.get('HTTP_AUTHORIZATION', b'')
            token = auth_token.split('.')
            payload = token[1] + "===="
            payload_data = base64.b64decode(payload).decode(encoding='utf-8')
            # print(payload_data)
            payload_dict = json.loads(payload_data)
            user = User.objects.get(id=payload_dict['user_id'])
        except:
            raise exceptions.AuthenticationFailed('token认证出错')

        if not user.check_password(request.data['password']):
            raise exceptions.AuthenticationFailed('密码错误')
        else:
            user.delete()
            return Response(status.HTTP_200_OK)


# 修改密码
class ChangePassWdAPIView(generics.GenericAPIView):
    serializer_class = UpdateSerializer
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
        except:
            raise exceptions.NotFound('用户不存在')

        try:
            old_password = request.data['old_password']
        except:
            raise exceptions.AuthenticationFailed("请输入原密码")

        if not user.check_password(old_password):
            raise exceptions.AuthenticationFailed('请保证原密码的正确性')

        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_304_NOT_MODIFIED)
