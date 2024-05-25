from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DRF.settings import strip_client
from course.docs import SUBSCRIBE_VIEW_SCHEMA
from course.filters import PaymentFilter
from course.models import Course, Lesson
from course.paginators import MyPagination
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment, Subscription
from users.permissions import IsModerator, IsOwnerOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwnerOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, ~IsModerator | IsOwnerOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrReadOnly]
        return super().get_permissions()


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['date']
    ordering = ['-date']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(user=self.request.user)

        if payment.method == Payment.translation:
            product_name = payment.course.name if getattr(payment, 'course') else payment.lesson.name
            product = strip_client.create_product(name=product_name)
            price = strip_client.create_price(
                name=product_name,
                price=payment.amount
            )
            session = strip_client.create_session(
                price_id=price['id'],
                success_url=request.build_absolute_uri(reverse('courses-list'))
            )
            return Response({'url': session.get("url")}, status=status.HTTP_201_CREATED)

        return Response({'url': reverse('courses-list')}, status=status.HTTP_201_CREATED)


class SubscriptionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SUBSCRIBE_VIEW_SCHEMA)
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=request.user, course=course_item)

        if subs_item.exists():
            subs_item[0].delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=request.user, course=course_item)
            message = 'подписка добавлена'
        return Response({"message": message})
