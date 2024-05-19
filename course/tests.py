import io

from PIL import Image
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course
from users.models import User, Subscription


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='r@r.ru',
            username='r',
            password='1234'
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': 'Тестовый курс',
            'preview': self.generate_image_file(),
            'description': 'Описание для тестового курса',
        }

    @staticmethod
    def generate_image_file():
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.name = 'test_image.jpg'
        file.seek(0)
        return file

    def create_course(self):
        response = self.client.post(reverse('courses-list'), self.data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data['id']


class CourseAPITestCase(BaseAPITestCase):

    def test_get_list_courses(self):
        response = self.client.get(reverse('courses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        response = self.client.post(reverse('courses-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_course(self):
        course_id = self.client.post(reverse('courses-list'), self.data).data['id']
        data = {
            'name': 'Обновленный курс',
            'preview': self.generate_image_file(),
            'description': 'Обновленное описание для тестового курса',
        }
        url = reverse('courses-detail', kwargs={'pk': course_id})
        response = self.client.patch(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Обновленный курс')
        self.assertEqual(response.data['description'], 'Обновленное описание для тестового курса')

    def test_delete_course(self):
        course_id = self.client.post(reverse('courses-list'), self.data).data['id']
        url = reverse('courses-detail', kwargs={'pk': course_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(pk=course_id).exists())

    @staticmethod
    def generate_image_file():
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(file, 'jpeg')
        file.name = 'test_image.jpg'
        file.seek(0)
        return file


class SubscriptionAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.course_id = self.create_course()
        self.url = reverse('subscribe', args=[self.course_id])

    def test_subscribe_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course_id=self.course_id).exists())

    def test_unsubscribe_user(self):
        response_create = self.client.post(self.url)
        response_delete = self.client.post(self.url)
        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course_id=self.course_id).exists())
