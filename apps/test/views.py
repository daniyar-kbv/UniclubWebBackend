from rest_framework.viewsets import ModelViewSet
from apps.users.models import User


class ClientViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class =