from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('map', views.MapPageView.as_view(), name="map_page"),
    path('api/', include("map.api.urls")),
]


