from django.urls import include, path
from rest_framework import routers

from course.views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView,
    SubscriptionCreateView
)

router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet, basename='courses')

urlpatterns = [
    path("", include(router.urls), name="courses"),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lessons-list"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lessons-detail",
    ),
    path("payments/", PaymentListCreateAPIView.as_view(), name='list_payments'),

    path("courses/<int:pk>/subscribe/", SubscriptionCreateView.as_view(), name='subscribe'),
]
