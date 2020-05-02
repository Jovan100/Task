from rest_framework.serializers import ModelSerializer
from calculation.models import Calculations

class CalculationsSerializer(ModelSerializer):
    class Meta:
        model = Calculations
        fields = '__all__'
        read_only_fields = ['pk', 'created_at', 'updated_at']
