from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="courses/previews/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "courses"
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    preview = models.ImageField(upload_to="lessons/previews/", verbose_name="Превью")
    description = models.TextField(verbose_name="Описание")
    url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс"
    )

    def __str__(self):
        return f"{self.name} - {self.course}"

    class Meta:
        db_table = "lessons"
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
