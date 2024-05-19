from django.urls import include, path
from rest_framework import routers

from course.views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    PaymentListAPIView,
    SubscriptionCreateView
)

router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lessons-list"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lessons-detail",
    ),
    path("payments/", PaymentListAPIView.as_view(), name='list_payments'),

    path("courses/<int:pk>/subscribe/", SubscriptionCreateView.as_view(), name='subscribe'),
]
