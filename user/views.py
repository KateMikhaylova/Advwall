from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.permissions import IsUser
from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    ViewSet class to provide CRUD operations with user instances
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update']:
            return [IsUser()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        if self.action == 'list':
            return [IsAdminUser()]
        return []

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def create(self, request, *args, **kwargs):
        response = self._check_passwords(request)
        if response:
            return response
        password = make_password(request.data.get('password'))
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if request.data.get('password'):
            current_password = request.data.get('current_password')
            if not check_password(current_password, request.user.password):
                return Response({"password": ["Invalid password."]},
                                status=status.HTTP_401_UNAUTHORIZED)
            response = self._check_passwords(request)
            if response:
                return response
            password = make_password(request.data.get('password'))
            self.perform_update(serializer, password=password)
        else:
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def _check_passwords(self, request):
        raw_password1 = request.data.get('password')
        raw_password2 = request.data.get('repeat_password')
        if not raw_password1:
            return Response({"password": ["This field is required."]},
                            status=status.HTTP_400_BAD_REQUEST)
        if not raw_password2:
            return Response({"repeat_password": ["This field is required."]},
                            status=status.HTTP_400_BAD_REQUEST)
        if raw_password1 != raw_password2:
            return Response({"password": ["Passwort fields does not correspond."]},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('current_password') and \
                (request.data.get('current_password') == raw_password1):
            return Response({"password": ["New passport should differ from old one."]},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(raw_password1)
            return None
        except ValidationError as errors:
            return Response({"password": list(errors)},
                            status=status.HTTP_400_BAD_REQUEST)
