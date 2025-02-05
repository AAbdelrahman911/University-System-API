import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from courses.models import Course, Enrollment
from grades.models import Grade
from attendance.models import Attendance
from decimal import Decimal
from datetime import date
from django.db import IntegrityError, transaction

class TestUserAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'student',
            'student_id': 'ST123'
        }
        
    def test_create_user(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.user_type, 'student')

class TestCourseSystem(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.professor = User.objects.create_user(
            username='prof1',
            email='prof@example.com',
            password='prof123',
            user_type='professor',
            first_name='John',
            last_name='Doe'
        )
        self.student = User.objects.create_user(
            username='student1',
            email='student@example.com',
            password='student123',
            user_type='student',
            student_id='ST456'
        )
        
        self.course = Course.objects.create(
            name='Test Course',
            code='TC101',
            professor=self.professor
        )

    def test_grade_creation(self):
        grade_data = {
            'student': self.student,
            'course': self.course,
            'score': Decimal('85.50')
        }
        grade = Grade.objects.create(**grade_data)
        self.assertEqual(grade.score, Decimal('85.50'))
        self.assertEqual(grade.student, self.student)
        self.assertEqual(grade.course, self.course)

    def test_attendance_tracking(self):
        attendance_data = {
            'student': self.student,
            'course': self.course,
            'date': date.today(),
            'present': True
        }
        attendance = Attendance.objects.create(**attendance_data)
        self.assertTrue(attendance.present)
        self.assertEqual(attendance.student, self.student)
        self.assertEqual(attendance.course, self.course)

    def test_user_unique_student_id(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    username='student2',
                    email='student2@example.com',
                    password='student123',
                    user_type='student',
                    student_id='ST456' 
                )

    def test_grade_unique_together(self):
        Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('90.00')
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Grade.objects.create(
                    student=self.student,
                    course=self.course,
                    score=Decimal('95.00')
                )

    def test_attendance_unique_together(self):
        Attendance.objects.create(
            student=self.student,
            course=self.course,
            date=date.today(),
            present=True
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Attendance.objects.create(
                    student=self.student,
                    course=self.course,
                    date=date.today(),
                    present=False
                )

    def test_enrollment_count(self):
        initial_count = self.student.enrollment_count
        Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        self.student.refresh_from_db()
        self.assertEqual(self.student.enrollment_count, initial_count + 1)

    def test_user_str_representation(self):
        expected_str = f'{self.professor.get_full_name()} (professor)'
        self.assertEqual(str(self.professor), expected_str)

class GradeCategoryTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student5', 
            password='testpass5', 
            user_type='student',
            student_id='ST911',
            email='student911@example.com'
        )

        self.course = Course.objects.create(
            name='Psychology', 
            code='PSY202', 
            professor=User.objects.create_user(
                username='prof235', 
                password='testpass6', 
                user_type='professor',
                email='prof2345@example.com'
            )
        )

    def test_grade_categories(self):
        test_cases = [
            (0.00, 'Failed'),
            (49.99, 'Failed'),
            (50.00, 'Approved'),
            (64.99, 'Approved'),
            (65.00, 'Good'),
            (79.99, 'Good'),
            (80.00, 'Very Good'),
            (89.99, 'Very Good'),
            (90.00, 'Excellent'),
            (100.00, 'Excellent'),
        ]

        grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('0.00')
        )

        for score, expected_category in test_cases:
            grade.score = Decimal(str(score))
            grade.save()
            self.assertEqual(grade.get_grade_category(), expected_category)