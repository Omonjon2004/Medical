# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.doctor.models import DoctorRating, Doctors
from .serializers import DoctorRatingSerializer


class RateDoctorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doctor_id):
        try:
            doctor = Doctors.objects.get(id=doctor_id)
        except Doctors.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        patient = request.user

        data = request.data.copy()
        data['doctor'] = doctor.id
        data['patient'] = patient.id

        rating, created = DoctorRating.objects.update_or_create(
            patient=patient,
            doctor=doctor,
            defaults={
                'rating': data.get('rating'),
            }
        )

        serializer = DoctorRatingSerializer(rating)
        message = "Rating updated" if not created else "Rating created"
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_200_OK)
