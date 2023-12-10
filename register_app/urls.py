from django.urls import path
from .views import *

urlpatterns = [
    path("cash_machine/", cash_machine, name="cash_machine")
]
