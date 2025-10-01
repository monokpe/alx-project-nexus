from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductCategoryChartView, redirect_to_products_by_category

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('chart/', ProductCategoryChartView.as_view(), name='product_category_chart'),
    path('category/<slug:category_slug>/', redirect_to_products_by_category, name='products_by_category'),
]