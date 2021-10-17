import ast
import uuid
from django.db import models

# Create your models here.


class Tutor(models.Model):
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.EmailField("email")
    verified = models.BooleanField(default=False)
    public_id = models.CharField(default=str(uuid.uuid4()), max_length=300)
    rating = models.CharField("[]", max_length=1300)  # a list of rating. Return mean of values
    courses = models.TextField("[]")    # a list of courses offered
    user_id = models.IntegerField(default=1000000)
    enrolled_courses = models.TextField("{}")   # a dict of courses enrolled {course_title: number_of_enrollment}
    active = models.BooleanField(default=True)

    def add_course(self, course_id):
        self.courses = str(ast.literal_eval(self.courses).append(course_id))

    def remove_course(self, course_id):
        self.courses = str(ast.literal_eval(self.courses).remove(course_id))

    def get_courses(self):
        return ast.literal_eval(self.courses)

    def add_enrolled_course(self, course_title):
        e_c = ast.literal_eval(self.enrolled_courses)
        if course_title in list(e_c.keys()):
            e_c[course_title] += 1
        else:
            e_c[course_title] = 1
        self.enrolled_courses = str(e_c)

    def get_enrolled_courses(self):
        return ast.literal_eval(self.enrolled_courses)

    def add_user_id(self, user_id):
        self.user_id = user_id

    def add_rating(self, rating):
        self.rating = str(ast.literal_eval(self.rating).append(rating))

    def get_rating(self):
        rating = ast.literal_eval(self.rating)
        total, count = sum(rating), len(rating)
        return round(total/count, 1)

