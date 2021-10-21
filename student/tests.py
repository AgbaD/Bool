from django.test import TestCase
from .models import Student


class StudentModelTest(TestCase):

    def test_get_cart(self):
        s = Student()
        s = s.get_cart()
        self.assertIsInstance(s, list)

    def test_clear_cart(self):
        s = Student()
        s.clear_cart()
        self.assertEqual(s.get_cart(), [])

    def test_get_wishlist(self):
        s = Student()
        s = s.get_wishlist()
        self.assertIsInstance(s, list)

    def test_clear_wishlist(self):
        s = Student()
        s.clear_wishlist()
        self.assertEqual(s.get_wishlist(), [])
