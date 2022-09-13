from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (AdminSerializer, SignUpSerializer,
                               TokenSerializer, UserSerializer)

from api_yamdb.settings import EMAIL_FROM


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = LimitOffsetPagination

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='me',
    )
    def me_page(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def send_confirmation_code(user, confirmation_code):
    send_mail(
        'Код активации YaMDb',
        f'Ваш код активации - {confirmation_code}',
        EMAIL_FROM,
        [user.email]
    )


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, _ = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_confirmation_code(user, user.confirmation_code)
    return Response(serializer.data)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    access = AccessToken.for_user(user)
    return Response(f'token: {access}')
