from django.core.management import BaseCommand

from course.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create_user(
            "root",
            "root@mail.ru",
            "root",
        )
        courses = [
            Course(
                name="Курс по рисованию",
                preview="/courses/previews/1.png",
                description="Полный курс по рисованию"
            ),
            Course(
                name="Курс по python",
                preview="/courses/previews/2.png",
                description="Полный курс по python"
            )
        ]
        lessons = [
            Lesson(
                name="Урок 1. Рисуем круги",
                preview="/lessons/previews/1.png",
                description="Учимся рисовать круги",
                url="https://les.com/krug",
                course_id=1
            ),
            Lesson(
                name="Урок 1. Переменные",
                preview="/lessons/previews/1.png",
                description="Что такое переменные",
                url="https://les.com/python",
                course_id=2
            )
        ]
        Course.objects.bulk_create(courses)
        Lesson.objects.bulk_create(lessons)
        Payment.objects.create(
            user=user,
            lesson_id=1,
            amount=1000,
            method=Payment.cash
        )
        Payment.objects.create(
            user=user,
            lesson_id=2,
            amount=20000,
            method=Payment.invoice
        )
