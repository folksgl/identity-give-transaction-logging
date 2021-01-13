""" Views for Transaction Logging API """
from rest_framework import viewsets
from .serializers import TransactionRecordSerializer
from .models import TransactionRecord


class TransactionRecordViewSet(viewsets.ModelViewSet):
    queryset = TransactionRecord.objects.all().order_by("record_uuid")
    serializer_class = TransactionRecordSerializer
