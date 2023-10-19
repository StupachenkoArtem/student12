from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from students.models import Group, Student
from students.serializers import StudentSerializer
from students.views import teachers, StudentHome, ShowStudent
from django.test import SimpleTestCase


def calc(a, b, c):
    if c == '+':
        return a + b
    if c == '-':
        return a - b
    if c == '*':
        return a * b


class LogicTestCase(TestCase):
    def test_plus(self):
        result = calc(5, 7, '+')
        self.assertEqual(12, result)

    def test_minus(self):
        result = calc(5, 7, '-')
        self.assertEqual(-2, result)


class StudentsApiTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(username='Flitz', password='Csdmfaceit0')
        self.user2 = User.objects.create_user(username='Flitz14', password='Csdmfaceit0')
        self.group1 = Group.objects.create(name='43', course='1', enrollment_year='2023')
        self.student1 = Student.objects.create(first_name='Иван', last_name='Зернов', middle_name='Иванович', email='ivan@mail.ru',
                                          group_id=self.group1.id, slug='zernov', user=self.user1)
        self.student2 = Student.objects.create(first_name='Екатерина', last_name='Смирнова', middle_name='Николаевна', email='katya@mail.ru',
                                          group_id=self.group1.id, slug='smirnova', user=self.user1)
        self.students_url = reverse('students-list')
        self.student_url = reverse('students-detail', kwargs={'pk': self.student1.pk})

    def test_get(self):
        response = self.client.get(self.students_url)
        serializer_data = StudentSerializer([self.student1, self.student2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])
        # print(f'{response.data}')

    def test_delete(self):
        self.client.force_login(self.user1)
        response = self.client.delete(self.student_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_post_student(self):
        self.client.force_login(self.user1)
        with open("students/scr5.png", 'rb') as pict:
            data = {
                'first_name': 'Екатерина',
                'last_name': 'Смирнова',
                'middle_name': 'Николаевна',
                'email': 'katya@mail.ru',
                'group': self.group1.id,
                'slug': 'smirnova1',
                'photo': pict,
                'user': self.user1.id
            }
            response = self.client.post(self.students_url, data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class StudentSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(username='Flitz', password='Csdmfaceit0')
        self.user2 = User.objects.create_user(username='Flitz14', password='Csdmfaceit0')
        self.group1 = Group.objects.create(name='43', course='1', enrollment_year='2023')
        self.student1 = Student.objects.create(first_name='Иван', last_name='Зернов', middle_name='Иванович',
                                           email='ivan@mail.ru',
                                           group_id=self.group1.id, slug='zernov', user=self.user1)
        self.student2 = Student.objects.create(first_name='Екатерина', last_name='Смирнова', middle_name='Николаевна',
                                           email='katya@mail.ru',
                                            group_id=self.group1.id, slug='smirnova', user=self.user1)
        self.students_url = reverse('students-list')
        self.student_url = reverse('students-detail', kwargs={'pk': self.student1.pk})

    def test_student_serializer(self):
        serializer_data = StudentSerializer([self.student1, self.student2], many=True).data
        expected_data = [
            {
                'last_name': 'Зернов',
                'first_name': 'Иван',
                'middle_name': 'Иванович',
                'email': 'ivan@mail.ru',
                'group': self.student1.group_id,
                'slug': 'zernov',
                'photo': None
            },
            {
                'last_name': 'Смирнова',
                'first_name': 'Екатерина',
                'middle_name': 'Николаевна',
                'email': 'katya@mail.ru',
                'group': self.student2.group_id,
                'slug': 'smirnova',
                'photo': None
            }
        ]
        self.assertEqual(expected_data, serializer_data)


class TestUrls(SimpleTestCase):

    def test_list_url_teachers(self):
        url = reverse('teachers')
        self.assertEqual(resolve(url).func, teachers)

    def test_list_url_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, StudentHome)

    def test_list_url_student(self):
        url = reverse('student', args=['smirnov'])
        self.assertEqual(resolve(url).func.view_class, ShowStudent)


class BasicTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret')

        self.group1 = Group.objects.create(
            name='43',
            course='1',
            enrollment_year='2023')

        self.student1 = Student.objects.create(
            first_name='Иван',
            last_name='Зернов',
            middle_name='Иванович',
            email='ivan@mail.ru',
            group_id=self.group1.id,
            slug='zernov',
            user=self.user1
        )

        self.updatestudent_url = reverse('update_student', args=['1'])
        self.addstudent_url = reverse('addstudent')
