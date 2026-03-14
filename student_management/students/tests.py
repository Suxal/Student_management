from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student

class StudentCRUDTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='test123')
        self.client.login(username='admin', password='test123')
        self.student = Student.objects.create(
            first_name='Alice', last_name='Smith',
            email='alice@test.com', course='CS', roll_number='CS001'
        )

    def test_list_view(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')

    def test_create_student(self):
        response = self.client.post(reverse('student-create'), {
            'first_name': 'Bob', 'last_name': 'Jones',
            'email': 'bob@test.com', 'course': 'Math',
            'roll_number': 'MT001'
        })
        self.assertEqual(Student.objects.count(), 2)

    def test_delete_student(self):
        response = self.client.post(reverse('student-delete', args=[self.student.pk]))
        self.assertEqual(Student.objects.count(), 0)