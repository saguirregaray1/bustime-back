from django.urls import path


from . import views

urlpatterns = [
    path("buses/", views.GetBusesView.as_view(), name="buses"),
    path("stops/", views.GetStopsView.as_view(), name="stops"),
    path("stops/<int:stop_id>/", views.GetStopInfoView.as_view(), name="stop_info"),
    path("auth/create/", views.CreateUserView.as_view(), name="create"),
    path("auth/token/", views.CreateTokenView.as_view(), name="token"),
    path("auth/me/", views.ManageUserView.as_view(), name="me"),
    path("user/favstop/", views.AddFavouriteStopView.as_view(), name="favstop"),
]
