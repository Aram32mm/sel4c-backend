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
router.register('activity', views.ActivityResponseView)

app_name = 'response'

urlpatterns = [
    path('', include(router.urls)),
    # Para el Forms
    path('retrieve-forms/', views.AllFormsQuestionResponsesView.as_view(), name ="all forms responses"),  # noqa
    path('add/forms-response/<int:question_id>/', views.CreateFormsQuestionResponseView.as_view(), name ="user question response"),  # noqa
    # Para marcar un modulo completado
    path('completed-module/<int:parent_activity_id>', views.PostModuleResponseCompletionView.as_view(), name ="complete activity module"),  # noqa
    path('complete-modules/', views.ListModuleResponseCompletionView.as_view(), name ="complete activity module"),  # noqa

]
