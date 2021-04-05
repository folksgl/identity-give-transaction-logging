""" Views for Transaction Logging API """
from rest_framework import viewsets, mixins
from rest_framework.parsers import JSONParser
from api.serializers import TransactionRecordSerializer
from api.models import TransactionRecord


class TransactionRecordViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ Views for TransactionRecord """

    queryset = TransactionRecord.objects.all()
    serializer_class = TransactionRecordSerializer
    parser_classes = [JSONParser]

    async def __call__(self):
        pass
