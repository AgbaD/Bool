from .models import CourseFiles
from django.test import TestCase
from .models import Tutor, Course


class TutorModelTests(TestCase):

    def test_get_enrolled_courses(self):
        t = Tutor()
        self.assertIsInstance(t.get_enrolled_courses(), dict)

    def test_get_rating(self):
        t = Tutor()
        self.assertIsInstance(t.get_rating(), float)


class CourseModelTests(TestCase):

    def test_add_discount(self):
        c = Course()
        c.add_discount(20)
        self.assertEqual(c.discount, True)

    def test_remove_discount(self):
        c = Course()
        c.remove_discount()
        self.assertEqual(c.discount, False)

    def test_get_rating(self):
        c = Course()
        self.assertIsInstance(c.get_rating(), float)


class CourseFileModelTest(TestCase):

    def test_get_links(self):
        c = CourseFiles()
        c = c.get_links()
        self.assertIsInstance(c, list)

