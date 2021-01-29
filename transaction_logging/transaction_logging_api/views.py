""" Views for Transaction Logging API """
from rest_framework import viewsets, mixins
from .serializers import TransactionRecordSerializer
from .models import TransactionRecord


class TransactionRecordViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TransactionRecord.objects.all()
    serializer_class = TransactionRecordSerializer
