
from django.urls import path

from style.views import StyleViewSet, UserStyleAPIView


urlpatterns = [
    path('shop/', StyleViewSet.as_view({'get': 'list'}), name='shop'),
    path('shop/<int:pk>/', StyleViewSet.as_view({'get': 'retrieve'}), name='shop'),
    path('userstyle/', UserStyleAPIView.as_view()),
]

