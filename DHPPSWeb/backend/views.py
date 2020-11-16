from rest_framework import viewsets

from backend.models import Accountinformation
from backend.serializers import AccountsSerializer
# Create your views here.


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Accountinformation.objects.all()
    serializer_class = AccountsSerializer
