from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError

from course.models import Course, Lesson
from course.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        filter_by_course = self.request.GET.get('filter_by_course')
        filter_by_lesson = self.request.GET.get('filter_by_lesson')
        payment_method = self.request.GET.get('payment_method')
        queryset = Payment.objects.all()
        if sort == 'date':
            queryset = queryset.order_by('date')
        elif sort == '-date':
            queryset = queryset.order_by('-date')
        if filter_by_course:
            queryset = queryset.filter(course_id__in=filter_by_course)
        if filter_by_lesson:
            queryset = queryset.filter(lesson_id__in=filter_by_lesson)
        if payment_method:
            if payment_method not in Payment.LIST_PAYMENTS:
                raise ValidationError({
                    'error': f'Please provide correct payment method: {Payment.LIST_PAYMENTS}'
                })
            queryset = queryset.filter(method=payment_method)
        return queryset

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        sort = self.request.GET.get('sort')
        filter_by_course = self.request.GET.get('filter_by_course')
        filter_by_lesson = self.request.GET.get('filter_by_lesson')
        payment_method = self.request.GET.get('payment_method')
        queryset = Payment.objects.all()
        if sort == 'date':
            queryset = queryset.order_by('date')
        elif sort == '-date':
            queryset = queryset.order_by('-date')
        if filter_by_course:
            queryset = queryset.filter(course_id__in=filter_by_course)
        if filter_by_lesson:
            queryset = queryset.filter(lesson_id__in=filter_by_lesson)
        if payment_method:
            if payment_method not in Payment.LIST_PAYMENTS:
                raise ValidationError({
                    'error': f'Please provide correct payment method: {Payment.LIST_PAYMENTS}'
                })
            queryset = queryset.filter(method=payment_method)
        return queryset
