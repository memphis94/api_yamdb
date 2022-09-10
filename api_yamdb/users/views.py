from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, filters, decorators, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_FROM
from users.models import User
from users.serializers import UserSerializer, SignUpSerializer, TokenSerializer


def send_confirmation_code(user):
    code = randint(100000, 999999)
    user.confirmation_code = code
    user.save()
    send_mail(
        'Код активации YaMDb',
        f'Ваш код активации - {code}',
        EMAIL_FROM,
        [user.email]
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @decorators.action(
        methods=['GET', 'PATCH'],
        detail=False,
        # url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me_page(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    user = User.objects.filter(email=email)

    if not user.exists():
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = user.get(email=email)
    send_confirmation_code(user)
    return Response(
        {'message': 'Пользователь с такой электронной почтой уже '
                    'существует. Код подтверждения отправлен повторно. '
         },
        status=status.HTTP_400_BAD_REQUEST
    )


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    access = AccessToken.for_user(user)
    return Response(f'token: {access}', status=status.HTTP_200_OK)
