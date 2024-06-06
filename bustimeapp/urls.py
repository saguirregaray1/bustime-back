from django.urls import path
from .views import GetBusesView, GetStopInfoView, GetStopsView


from . import views

urlpatterns = [
    path("buses/", GetBusesView.as_view(), name="buses"),
    path("stops/", GetStopsView.as_view(), name="stops"),
    path("stops/<int:stop_id>/", GetStopInfoView.as_view(), name="stop_info"),
    path("auth/create/", views.CreateUserView.as_view(), name="create"),
    path("auth/token/", views.CreateTokenView.as_view(), name="token"),
    path("auth/me/", views.ManageUserView.as_view(), name="me"),
]
