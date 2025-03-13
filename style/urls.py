
from django.urls import path

from style.views import StyleViewSet


urlpatterns = [
    path('', StyleViewSet.as_view({'get': 'list'}), name='shop'),
    path('<int:pk>/', StyleViewSet.as_view({'get': 'retrieve'}), name='shop'),
]

