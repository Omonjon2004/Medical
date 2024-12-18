from rest_framework import serializers

from apps.medication.models import Medications, Medication_Rating


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medications
        fields = (
            'id',
            'name',
            'description',
            'dosage_form',
            'strength',
            'price',
            'stock_quantity',
            'manufacturer',
            'total_rating',
            'rating_count',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'id': {'read_only': True},
        }

class MedicationRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication_Rating
        fields = ['user', 'medication', 'rating']
        extra_kwargs = {
            'user': {'read_only': True},
        }
