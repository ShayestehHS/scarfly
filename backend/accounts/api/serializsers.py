from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

UPDATE_LAST_LOGIN = getattr(settings, 'UPDATE_LAST_LOGIN', False)
RETURN_EXPIRATION = getattr(settings, 'RETURN_EXPIRATION', False)
USER = get_user_model()


class LoginRegisterSerializer(serializers.Serializer):
    default_error_messages = {'no_active_account': 'No active account found with the given credentials'}
    phone_number = serializers.CharField(min_length=13, max_length=13, allow_null=False, write_only=True)

    def validate_phone_number(self, value):
        if value[:4] != "+989":
            raise ValidationError({"detail": "Phone number should start with with '+989'"})
        return value

    @staticmethod
    def validate_user(user):
        msg = None
        if user is None:
            msg = 'Unable to log in with provided credentials.'
        elif not user.is_active:
            msg = 'User account is disabled.'
        if msg is not None:
            raise ValidationError({'detail': msg})

    def to_representation(self, instance):
        if not isinstance(instance, USER):
            # Login
            phone_number = instance.get('phone_number')
            user = get_user_model().objects.filter(phone_number=phone_number).first()
            self.validate_user(user)
        else:
            # Register
            user = instance

        token = RefreshToken().for_user(user)
        data = {'access': str(token.access_token), 'refresh': str(token)}

        if UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        if RETURN_EXPIRATION:
            data.update({
                'access_expiration': token.access_token.get('exp'),
                'refresh_expiration': token.get('exp')
            })

        return data

    def create(self, validated_data):
        try:
            user = get_user_model().objects.create_user(phone_number=validated_data['phone_number'])
        except IntegrityError:
            raise ValidationError({'duplicated': 'An user with this phone number already exists'})

        return user


class RetrieveUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['first_name', 'last_name', 'phone_number']

