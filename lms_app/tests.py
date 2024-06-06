from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms_app.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    """Тест для модели Course"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        """Тест создания курса"""
        url = reverse('lms_app:course-list')
        data = {'name': 'Test Course 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_list(self):
        """Тест вывода списка курсов"""
        url = reverse('lms_app:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.pk,
                    'lessons_count': 1,
                    'lessons': [
                        {'id': self.lesson.pk,
                         'video_link': None,
                         'name': 'Test Lesson',
                         'description': None,
                         'preview': None,
                         'course': self.course.pk,
                         'owner': self.user.pk
                         }
                    ],
                    'is_subscribed': False,
                    'name': 'Test Course',
                    'preview': None,
                    'description': None,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_course_retrieve(self):
        """Тест вывода одного курса"""
        url = reverse('lms_app:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': self.course.pk,
            'lessons_count': 1,
            'lessons': [
                {
                    'id': self.lesson.pk,
                    'video_link': None,
                    'name': 'Test Lesson',
                    'description': None,
                    'preview': None,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ],
            'is_subscribed': False,
            'name': 'Test Course',
            'preview': None,
            'description': None,
            'owner': self.user.pk
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_course_update(self):
        """Тест обновления курса"""
        url = reverse('lms_app:course-detail', args=(self.course.pk,))
        data = {'name': 'Test Course New'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test Course New')

    def test_course_delete(self):
        """Тест удаления курса"""
        url = reverse('lms_app:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestCase(APITestCase):
    """Тест для модели Lesson"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('lms_app:lesson-create')
        data = {'name': 'Test Lesson 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_list(self):
        """Тест вывода списка уроков"""
        url = reverse('lms_app:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'video_link': None,
                    'name': 'Test Lesson',
                    'description': None,
                    'preview': None,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        """Тест вывода одного урока"""
        url = reverse('lms_app:lesson-get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': self.lesson.pk,
            'video_link': None,
            'name': 'Test Lesson',
            'description': None,
            'preview': None,
            'course': self.course.pk,
            'owner': self.user.pk
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_update(self):
        """Тест изменения урока"""
        url = reverse('lms_app:lesson-update', args=(self.lesson.pk,))
        data = {'name': 'Lesson New'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Lesson New')

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse('lms_app:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_bad_video_url(self):
        """Тест добавления в урок запрещенной ссылки"""
        url = reverse('lms_app:lesson-update', args=(self.lesson.pk,))
        data = {'video_link': 'Cool_url_link'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data.get('video_link'), [
            "В поле 'video_link' присутствует запрещенная ссылка. Допускаются только ссылки на https://youtube.com/",
            'Введите правильный URL.'])


class SubscriptionTestCase(APITestCase):
    """Тест для модели Subscription"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        """Тест добавления и удаления подписки на курс"""
        url = reverse('lms_app:subscription')
        data = {'course': self.course.pk}

        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json(), {"message": "Подписка добавлена"})
        self.assertEqual(Subscription.objects.all().count(), 1)

        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json(), {"message": "Подписка удалена"})
        self.assertEqual(Subscription.objects.all().count(), 0)


class LessonManagerTestCase(APITestCase):
    """Тест для модели Lesson с пользователем модератор"""

    def setUp(self):
        self.user = User.objects.create(email='moderator@test.ru', is_staff=True)
        self.my_group = Group.objects.create(name="moderators")
        self.user.groups.add(self.my_group)
        self.lesson = Lesson.objects.create(name='Test Lesson')
        self.client.force_authenticate(user=self.user)

    def test_lesson_create_moderator(self):
        """Тест создания урока модератором"""
        url = reverse('lms_app:lesson-create')
        data = {'name': 'Test Lesson 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_delete_moderator(self):
        """Тест удаления урока модератором"""
        url = reverse('lms_app:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)
