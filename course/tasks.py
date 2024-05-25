from django.core.mail import send_mail

from DRF.celery import app


@app.task
def send_mail_update_course(course_id):
    send_mail(
        'Course Updated',
        f'The course "1',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
