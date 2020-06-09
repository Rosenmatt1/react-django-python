from chuck.models import Chuck
from rest_framework import viewsets, permissions
from .serializers import ChuckSerializer

#Lead Viewset
class ChuckViewSet(viewsets.ModelViewSet):
    queryset = Chuck.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ChuckSerializer    