"""
Views para Respuestas de Usuarios a Actividades y Preguntas
"""
from rest_framework import viewsets, generics, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import ActivityResponse, FormsQuestionResponse
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from core.models import FormsQuestion, Activity, User
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)


from response.serializers import (
    ActivityResponseSerializer,
    FormsQuestionResponseSerializer,
)


class AllFormsQuestionResponsesView(generics.ListAPIView):
    """Permite a Usuario/Admin Ver Respuestas Del Forms"""
    serializer_class = FormsQuestionResponseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_admin = self.request.user.is_staff

        if is_admin:
            queryset = FormsQuestionResponse.objects.all().order_by('user__id')
        else:
            queryset = FormsQuestionResponse.objects.filter(user=self.request.user).order_by('question__id')  # noqa

        return queryset


class CreateFormsQuestionResponseView(generics.CreateAPIView):
    """Permite a Usuario Postear Respuestas Del Forms"""
    serializer_class = FormsQuestionResponseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(FormsQuestion, pk=question_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, question=question)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'user_id',
                OpenApiTypes.INT,
                description='User ID to Filter Responses By User',
            ),
            OpenApiParameter(
                'activity_id',
                OpenApiTypes.INT,
                description='Activity ID to Filter Responses By Actvitity',
            ),
            OpenApiParameter(
                'response_type',
                OpenApiTypes.STR,
                description='Response Type to Filter Responses By Type',
            ),
        ]
    )
)
class ActivityResponseView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Vista para Obtener Respuestas de Actividades"""
    serializer_class = ActivityResponseSerializer
    queryset = ActivityResponse.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        activity_id = self.request.query_params.get('activity_id')
        response_type = self.request.query_params.get('response_type')

        queryset = self.queryset
        main_user = self.request.user

        if main_user.is_superuser:
            if user_id:
                user = get_object_or_404(User, pk=user_id)
                queryset = queryset.filter(user=user)
            if activity_id:
                activity = get_object_or_404(Activity, pk=activity_id)
                queryset = queryset.filter(activity=activity)
            if response_type:
                queryset = queryset.filter(response_type=response_type)

            queryset = queryset.order_by('user__id')
        else:
            queryset = queryset.filter(user=main_user).order_by('activity__id')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        activity_id = kwargs.get('pk')
        activity_object = get_object_or_404(Activity, id=activity_id)

        if request.user.is_superuser:
            response_instances = ActivityResponse.objects.filter(activity=activity_object).order_by('user__id')  # noqa
        else:
            response_instances = ActivityResponse.objects.filter(activity=activity_object, user=request.user).order_by('activity__id')  # noqa

        if not response_instances.exists():
            return Response({"error": "Responses not found for the given activity ID."}, status=status.HTTP_404_NOT_FOUND)  # noqa

        serializer = self.get_serializer(response_instances, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='upload-response')
    def create_response(self, request, pk=None):
        """Crea una respuesta"""
        user = self.request.user
        activity_object = get_object_or_404(Activity, id=pk)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, activity=activity_object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True, url_path='update-response')
    def update_response(self, request, pk=None):
        """Actualiza una respuesta existente"""
        user = self.request.user
        activity_object = get_object_or_404(Activity, id=pk)

        # checa que exista una respuesta a la actividad
        try:
            activity_response = ActivityResponse.objects.get(user=user, activity=activity_object)  # noqa
        except ActivityResponse.DoesNotExist:
             return Response({"error": "Response not found for the given activity ID."}, status=status.HTTP_404_NOT_FOUND)  # noqa

        # checa que el tipo de dato no se cambie
        current_data_type = activity_response.response_type
        new_response_type = request.data.get('response_type')

        if new_response_type and new_response_type != current_data_type:
            return Response({"error": "You cannot update the response type"}, status=status.HTTP_400_BAD_REQUEST)  # noqa

        serializer = self.get_serializer(activity_response, data=request.data, partial=True)  # noqa
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, activity=activity_object)
        return Response(serializer.data)
