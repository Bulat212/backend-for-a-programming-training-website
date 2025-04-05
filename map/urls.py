from django.urls import include, path

# from map.views import ProjectConnectionAPIView, ProjectConnectionViewSet

from map.views import *


# router = SimpleRouter()
# router.register(r'connectionViewSet', ProjectConnectionViewSet)

urlpatterns = [
    
    path('connection/', ProjectConnectionListAPIView.as_view()),
    path('elements/', MapElementsView.as_view()),
    path('user-project-map/', UserProjectMapView.as_view()),
    path('admin-create-map/', AdminMapCreateAPIView.as_view()),
    path('admin-list-map-project/', AdminProjectListAPIView.as_view()),
    
    
]

