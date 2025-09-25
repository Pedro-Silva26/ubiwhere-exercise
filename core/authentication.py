from rest_framework import authentication, exceptions

from core.models import SensorTokenAuth


class SensorTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('api-key')
        if not api_key:
            raise exceptions.AuthenticationFailed('api-key is required')

        try:
            token = SensorTokenAuth.objects.get(token=api_key, is_active=True)
        except SensorTokenAuth.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token is invalid or expired')

        return token, None
