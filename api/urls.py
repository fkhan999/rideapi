from django.urls import path
from api import views

urlpatterns = [
    path('', views.home),
    path('asset_req/',views.asset_req),
    path('rider_req/',views.rider_req),
    path('asset_req_get/',views.asset_req_get),
    path('match/',views.match),
    path('rider_select/',views.rider_select),
    

]