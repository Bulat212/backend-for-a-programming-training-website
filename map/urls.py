from django.urls import include, path

from rest_framework.routers import SimpleRouter
# from map.views import ProjectConnectionAPIView, ProjectConnectionViewSet

from map.views import MapElementsView, ProjectConnectionListAPIView


# router = SimpleRouter()
# router.register(r'connectionViewSet', ProjectConnectionViewSet)

urlpatterns = [
    
    path('connection/', ProjectConnectionListAPIView.as_view()),
    path('elements/', MapElementsView.as_view()),
    
    


    # path('connectionAPIView/', ProjectConnectionAPIView.as_view()),
    # path('connectionViewSet/', ProjectConnectionViewSet.as_view({'get': 'list'})),
    # path('', include(router.urls)),
]

