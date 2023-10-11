"""
Asignaciones de URL para la API de usuario
"""
from django.urls import path, include
from user import views


app_name = 'user'

urlpatterns = [
    # Crea usuario
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('admin/create/', views.CreateAdminView.as_view(), name='create_admin'),  # noqa
    path('deactivate/<int:user_id>/', views.deactivate_user, name='deactivate-user'),  # noqa
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),  # noqa
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),  # noqa

    # Genera token
    path('token/', views.CreateTokenView.as_view(), name='token'),
    # Administra usuario autenticado
    path('me/', views.ManageUserView.as_view(), name='me'),

    # agrega info al usuario
    path('info/add/', views.UserPersonalDataCreateView.as_view(), name='add_info'),  # noqa
    # Administra info de autenticado
    path('info/me/', views.UserPersonalDataView.as_view(), name='info'),

    # Recaba informaciones para admins
    path('info/all/', views.users_info, name='all_user_info'),
    path('admin/info/all/', views.admins_info, name='all_admin_info'),

    # Agrega scores iniciales
    path('scores/initial/', views.UserInitialScorePostView.as_view(), name='initial_scores'),  # noqa
    # Agrega scores finales
    path('scores/final/', views.UserFinalScorePostView.as_view(), name='final_scores'),  # noqa
]
