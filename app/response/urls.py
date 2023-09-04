"""
Mapeo de URL para Respuestas de Usuarios a Actividades y Preguntas
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from response import views


router = DefaultRouter()
router.register('activity', views.ActivityResponseViewSet)
router.register('question', views.FormsQuestionResponseViewSet)

app_name = 'response'

urlpatterns = [
    path('', include(router.urls)),
    path('activities-responses/', views.AllActivitiesResponsesView.as_view(), name ="activites responses"),  # noqa
    path('questions-responses/', views.AllFormsQuestionResponsesView.as_view(), name ="questions responses"),  #noqa

]
