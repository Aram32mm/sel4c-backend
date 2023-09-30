"""
Django Admin Personalizado
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Defininiendo la pagina de admin para admins."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal Info'),
            {
                'fields': (
                    'name',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )
    readonly_fields = ['last_login', 'date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class UserDataAdmin(admin.ModelAdmin):
    """Defininiendo la pagina admin de user data"""
    fields = ['user', 'full_name', 'academic_degree',
              'institution', 'gender', 'age', 'country', 'discipline']
    """
    readonly_fields = ['id', 'user', 'full_name', 'academic_degree',
                       'institution', 'gender', 'age', 'country', 'discipline']

    """

    class Meta:
        model = models.UserData


class UserInitialScoreAdmin(admin.ModelAdmin):
    fields = ['user', 'self_control_score', 'leadership_score',
              'consciousness_and_social_value_score',
              'social_innovation_and_financial_sustainability_score',
              'systemic_thinking_score', 'scientific_thinking_score',
              'critical_thinking_score', 'innovative_thinking_score']
    """
    readonly_fields = ['user', 'self_control_score', 'leadership_score',
                       'consciousness_and_social_value_score',
                       'social_innovation_and_financial_sustainability_score',
                       'systemic_thinking_score', 'scientific_thinking_score',
                       'critical_thinking_score', 'innovative_thinking_score']
    """

    class Meta:
        model = models.UserInitialScore


class UserFinalScoreAdmin(admin.ModelAdmin):
    fields = ['user', 'self_control_score', 'leadership_score',
              'consciousness_and_social_value_score',
              'social_innovation_and_financial_sustainability_score',
              'systemic_thinking_score', 'scientific_thinking_score',
              'critical_thinking_score', 'innovative_thinking_score']
    """
    readonly_fields = ['user', 'self_control_score', 'leadership_score',
                       'consciousness_and_social_value_score',
                       'social_innovation_and_financial_sustainability_score',
                       'systemic_thinking_score', 'scientific_thinking_score',
                       'critical_thinking_score', 'innovative_thinking_score']
    """
    class Meta:
        model = models.UserFinalScore


class ActivityAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'description', 'parent_activity']
    readonly_fields = ['id']

    class Meta:
        model = models.Activity


class FormsQuestionAdmin(admin.ModelAdmin):
    fields = ['id', 'question', 'description']
    readonly_fields = ['id']

    class Meta:
        model = models.FormsQuestion


class FormsQuestionResponseAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'question', 'score', 'time_minutes']
    readonly_fields = ['id', 'user', 'question', 'score', 'time_minutes']

    class Meta:
        model = models.FormsQuestionResponse


class ActivityResponseAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'activity', 'response_type',
              'string_response', 'image_response', 'video_response',
              'audio_response', 'time_minutes']
    readonly_fields = ['id', 'user', 'activity', 'response_type',
                       'string_response', 'image_response', 'video_response',
                       'audio_response', 'time_minutes']

    class Meta:
        model = models.ActivityResponse


admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserData, UserDataAdmin)
admin.site.register(models.UserInitialScore, UserInitialScoreAdmin)
admin.site.register(models.UserFinalScore, UserFinalScoreAdmin)

admin.site.register(models.FormsQuestion, FormsQuestionAdmin)
admin.site.register(models.FormsQuestionResponse, FormsQuestionResponseAdmin)

admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.ActivityResponse, ActivityResponseAdmin)
