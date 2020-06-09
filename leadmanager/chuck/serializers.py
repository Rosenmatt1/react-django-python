from rest_framework import serializers
from chuck.models import Chuck

#Chuck Serializer

class ChuckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chuck
        fields = ('__all__')