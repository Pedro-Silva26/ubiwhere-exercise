from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.SensorTokenAuthentication'
    name = 'ApiKeyAuth'

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "api-key",
        }


class BasicAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework.authentication.BasicAuthentication'
    name = 'BasicAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'basic'
        }
