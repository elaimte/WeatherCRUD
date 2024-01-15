from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import UserCollection
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, TokenBackendError
from rest_framework_simplejwt.state import token_backend
from datetime import timedelta

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['user_id'] = str(user.id)
        token.set_exp(lifetime=timedelta(hours=12))
        # token.payload['user_id'] = str(user.id)
        return token
    

class CustomRefreshToken(RefreshToken):
    access_token_class = CustomAccessToken
    @classmethod
    def for_user(cls, user):
        access_token = CustomAccessToken.for_user(user)
        instance = cls()
        instance['access_token'] = str(access_token)
        # return cls()
        return instance


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        raw_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        if raw_token == '':
            return None

        try:
            validated_token = token_backend.decode(raw_token, verify=True)
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed('Invalid token')
        except TokenBackendError as e:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user_id = validated_token.get('user_id')
            user = UserCollection.objects.get(id=user_id)
        except UserCollection.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)