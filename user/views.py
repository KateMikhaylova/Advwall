from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from user.models import User
from user.serializers import UserSerializer
from user.permissions import IsUser


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            return [IsUser()]
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def create(self, request, *args, **kwargs):
        raw_password1 = request.data.get('password')
        raw_password2 = request.data.get('repeat_password')
        if not raw_password1 or not raw_password2:
            return Response({"password": ["This fields are required."]}, status=status.HTTP_400_BAD_REQUEST)
        if raw_password1 != raw_password2:
            return Response({"password": ["Passport fields does not correspond."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(raw_password1)
        except ValidationError as errors:
            return Response({"password": [error for error in errors]}, status=status.HTTP_400_BAD_REQUEST)
        password = make_password(raw_password1)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, password=password)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        # TODO close all advertisements
        # TODO delete users authtoken???
        return Response(status=status.HTTP_204_NO_CONTENT)
