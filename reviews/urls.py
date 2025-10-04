from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
# The empty string prefix is important here as the path prefix is handled
# by the parent URL configuration that includes this file.
router.register(r'', ReviewViewSet, basename='review')

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls
