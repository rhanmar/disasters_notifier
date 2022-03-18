from django.urls import include, path

from map import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('map', views.MapPageView.as_view(), name="map_page"),
    path('api/', include("map.api.urls")),
]


