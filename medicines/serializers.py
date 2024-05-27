from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Medicine


class MedicineSerializer(ModelSerializer):

    class Meta:
        model = Medicine
        fields = (
            "name",
            "company",
            "price",
        )
