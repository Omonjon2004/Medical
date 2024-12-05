from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import (
    CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView)
from apps.doctor.api_endpoints.serializers import (
    DoctorCreateSerializer, DoctorUpdateSerializer, DoctorListSerializer)
from apps.doctor.models import Doctors

get_queryset = Doctors.objects.all()


class DoctorCreateAPIView(CreateAPIView):
    serializer_class = DoctorCreateSerializer
    queryset = get_queryset


class DoctorUpdateAPIView(UpdateAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = get_queryset


class DoctorListAPIView(ListAPIView):
    queryset = get_queryset
    serializer_class = DoctorListSerializer

    @method_decorator(cache_page(60 * 5))  # 5 daqiqa davomida keshlanadi
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class DoctorDestroyAPIView(DestroyAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = get_queryset
