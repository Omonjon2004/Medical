from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets,status
from rest_framework.generics import (
    CreateAPIView,  UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.doctor.api_endpoints.doctor_crud.serializers import (
    DoctorCreateSerializer, DoctorUpdateSerializer,
    DoctorListSerializer, DoctorDetailSerializer, DoctorRatingSerializer, )
from apps.doctor.models import Doctors
from config.permissions import IsDoctorReadOnly

get_queryset = Doctors.objects.all()


class DoctorCreateAPIView(CreateAPIView):
    serializer_class = DoctorCreateSerializer
    queryset = Doctors.objects.all()
    permission_classes = [IsDoctorReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorUpdateAPIView(UpdateAPIView):
    serializer_class = DoctorUpdateSerializer
    queryset = get_queryset
    permission_classes = [IsDoctorReadOnly]



class DoctorListAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoctorListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctors.objects.all().order_by('-ratings')


class DoctorDestroyAPIView(DestroyAPIView):
    serializer_class = DoctorDetailSerializer
    queryset = get_queryset
    permission_classes = [IsDoctorReadOnly]

class DoctorRatingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DoctorRatingSerializer,
    )
    def post(self, request):
        serializer = DoctorRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


