from random import randint
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, filters, decorators, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import EMAIL_FROM
from users.models import User
from users.permissions import IsRoleAdmin
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsRoleAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @decorators.action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated]
    )
    def me_page(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    user = User.objects.filter(username=username)
    if user.exists():
        return Response(
            {'message': 'Пользователь с таким именем уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = User.objects.filter(email=email)
    if user.exists():
        return Response(
            {'message': 'Пользователь с таким email уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    user, created = User.objects.get_or_create(
        username=username,
        email=email
    )
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@decorators.api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    access = AccessToken.for_user(user)
    return Response(f'token: {access}', status=status.HTTP_200_OK)
