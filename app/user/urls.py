"""
Asignaciones de URL para la API de usuario
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    # Crea usuario
    path('create', views.CreateUserView.as_view(), name='create'),
    path('create/with-permissions', views.CreateAdminView.as_view(), name='create'),  # noqa

    # Genera token
    path('token/', views.CreateTokenView.as_view(), name='token'),
    # Administra usuario autenticado
    path('me/', views.ManageUserView.as_view(), name='me'),

    # agrega info al usuario
    path('info/add/', views.UserPersonalDataCreateView.as_view(), name='add_info'),  # noqa
    # Administra info de autenticado
    path('info/me', views.UserPersonalDataView.as_view(), name='info'),

    # Recaba informaciones para admins
    path('info/all', views.users_info, name='all_info'),

    # Agrega scores iniciales
    path('scores/initial', views.UserInitialScorePostView.as_view(), name='initial_scores'),  # noqa
    # Agrega scores finales
    path('scores/final', views.UserFinalScorePostView.as_view(), name='final_scores'),  # noqa
]
