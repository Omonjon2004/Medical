from django.urls import path
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# Schema view konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="Poll API",
        default_version="v1",
        description="API for managing polls",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Swagger uchun URL manzillar
swagger_urlpatterns = [
    path(
        "swagger.json/",
        schema_view.without_ui(cache_timeout=0),  # JSON format
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),  # Swagger UI
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),  # ReDoc UI
        name="schema-redoc",
    ),
]

# Agar custom schema kerak bo'lsa
class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(self.view, "my_tags", [])
        if not tags:
            tags = [operation_keys[0]]  # Default tag is the first operation key
        return tags
