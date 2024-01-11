from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, NewsViewSet, AdvertisementViewSet, SaleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'news', NewsViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
