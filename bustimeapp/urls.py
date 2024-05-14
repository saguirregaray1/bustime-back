from django.urls import path
from .views import GetBusesView


from . import views

urlpatterns = [
    path('buses/', GetBusesView.as_view(), name='buses'),
]