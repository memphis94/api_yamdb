from django.shortcuts import get_object_or_404

from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя me недоступно'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        # extra_kwargs = {
        #     'username': {
        #         'validators': []
        #     }
        # }

    def validate(self, data):
        username = data['username']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Не совпадает код')
        return data


class UserSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = SignUpSerializer.Meta.fields + (
            'first_name', 'last_name', 'bio', 'role'
        )