from rest_framework import routers
from .api import ChuckViewSet

router = routers.DefaultRouter()
router.register('api/chuck', ChuckViewSet, 'chuck')

urlpatterns = router.urls

# from .api import LeadViewSet

# router = routers.DefaultRouter()
# router.register('api/leads', LeadViewSet, 'leads')

# urlpatterns = router.urls