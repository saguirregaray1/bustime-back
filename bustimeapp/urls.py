from django.urls import path
from .views import GetBusesView, GetStopInfoView, GetStopsView


from . import views

urlpatterns = [
    path('buses/', GetBusesView.as_view(), name='buses'),
    path('stops/', GetStopsView.as_view(), name='stops'),
    path('stops/<int:stop_id>/', GetStopInfoView.as_view(), name='stop_info'),
]