from rest_framework import serializers

from apps.medication.models import Medications


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
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'id': {'read_only': True},
        }
