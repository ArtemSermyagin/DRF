from django.core.mail import send_mail

from DRF.celery import app
from DRF.settings import EMAIL_HOST_USER
from course.models import Course
from users.models import Subscription


@app.task
def send_mail_update_course(course_id):
    course = Course.objects.get(pk=course_id)
    subscriptions = Subscription.objects.filter(course=course)
    recipient_list = [subscription.user.email for subscription in subscriptions]
    send_mail(
        'Course Updated',
        f'The course {course.name} has been updated.',
        EMAIL_HOST_USER,
        recipient_list,
    )
