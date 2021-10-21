import ast
import uuid
from django.db import models

# Create your models here.


class Student(models.Model):
    firstname = models.CharField(max_length=33)
    lastname = models.CharField(max_length=33)
    email = models.EmailField("email")
    phone = models.CharField(max_length=33)
    headline = models.TextField(default="headline")
    public_id = models.CharField(default=str(uuid.uuid4()), max_length=300)
    user_id = models.IntegerField(default=10000000)
    active = models.BooleanField(default=True)
    # many to many relationship
    courses = models.ManyToManyField('tutor.Course', related_name='students', blank=True)
    fav_courses = models.ManyToManyField('tutor.Course', related_name='students_fav', blank=True)
    # a list of courses
    cart = models.TextField(default='[]')
    wishlist = models.TextField(default='[]')

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

    def add_to_cart(self, course_id):
        if self.cart == '[]':
            self.cart = str([course_id])
        else:
            ca = ast.literal_eval(self.cart)
            ca.append(course_id)
            self.cart = str(ca)

    def get_cart(self):
        return ast.literal_eval(self.cart)

    def clear_cart(self):
        self.cart = "[]"

    def add_to_wishlist(self, course_id):
        if self.wishlist == '[]':
            self.wishlist = str([course_id])
        else:
            wl = ast.literal_eval(self.wishlist)
            wl.append(course_id)
            self.wishlist = str(wl)

    def get_wishlist(self):
        return ast.literal_eval(self.wishlist)

    def clear_wishlist(self):
        self.wishlist = "[]"


# class Notifications(models.Model):
#     subject = models.CharField(max_length=33)
#     note = models.TextField("Notification")
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     sender = models.CharField(default='admin', max_length=300)
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['created_on']
