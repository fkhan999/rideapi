from django.urls import path
from api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.home),
    path('create_user/', views.createUser),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('asset_req/',views.asset_req),
    path('rider_req/',views.rider_req),
    path('asset_req_get/',views.asset_req_get),
    path('match/',views.match),
    path('rider_select/',views.rider_select),
    

]