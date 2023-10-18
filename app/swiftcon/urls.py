"""
Asignaciones de URL para la API de Swift Connection
"""
from django.urls import path

from swiftcon import views

app_name = 'swiftcon'

urlpatterns = [
    path('user-default/add', views.CreateUserUserDefaultsView.as_view(), name="post user defaults"),  # noqa
    path('user-default/', views.RetrieveUpdateUserUserDefaultsView.as_view(), name="get/update user defaults"),  # noqa
]
