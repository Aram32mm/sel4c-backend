"""
URL configuration for SEL4C project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views


urlpatterns = [
    path('', core_views.index_page, name='index'),
    path('admin/', admin.site.urls),
    path('api/health-check/', core_views.health_check, name='health-check'),
    path('sel4c/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'sel4c/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('sel4c/user/', include('user.urls')),
    path('sel4c/methodology/', include('methodology.urls')),
    path('sel4c/response/', include('response.urls')),
    path('sel4c/swift-connection/', include('swiftcon.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
