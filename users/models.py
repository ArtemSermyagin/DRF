from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'



class Payment(models.Model):
    cash = 'cash'
    translation = 'translation'
    invoice = 'invoice'

    TYPE_PAYMENTS = (
        (cash, 'Наличные'),
        (translation, 'Перевод'),
        (invoice, 'Счет')
    )

    LIST_PAYMENTS = [
        cash, translation, invoice
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Курс'
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Урок'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма'
    )
    method = models.CharField(
        max_length=20,
        choices=TYPE_PAYMENTS,
        default=cash,
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f'{self.user} - {self.cash}'

    class Meta:
        db_table = "payments"
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
