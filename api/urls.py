""" Transaction logging API URLs """
from rest_framework import routers
from api.views import TransactionRecordViewSet

router = routers.DefaultRouter()
router.register(r"transaction", TransactionRecordViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = router.urls
