from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'core.authentication.SensorTokenAuthentication'
    name = 'ApiKeyAuth'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "api-key",
        }

    def get_security_requirement(self, auto_schema):
        return [{"ApiKeyAuth": []}]
