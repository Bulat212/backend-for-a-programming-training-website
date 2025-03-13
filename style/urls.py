
from django.urls import path

from style.views import StyleList


urlpatterns = [
    path('', StyleList.as_view(), name='shop'),

]

