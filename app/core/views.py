"""
Vistas para el CORE.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

@extend_schema
@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
