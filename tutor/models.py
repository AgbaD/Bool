import ast
from django.db import models

# Create your models here.


class Tutor(models.Model):
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)
    email = models.EmailField("email")
    verified = models.BooleanField(default=False)
    rating = models.CharField(max_length=1300)  # a list of rating. Return mean of values
    courses = models.TextField("[]")    # a list of courses offered
    user_id = models.IntegerField(default=1000000)
    enrolled_courses = models.TextField("{}")   # a list of courses enrolled for

    def add_course(self, course_id):
        self.courses = str(ast.literal_eval(self.courses).append(course_id))

    def remove_course(self, course_id):
        self.courses = str(ast.literal_eval(self.courses).remove(course_id))

    def add_enrolled_courses(self, course_id):
        self.enrolled_courses = str(ast.literal_eval(self.enrolled_courses).append(course_id))

    def add_user_id(self, user_id):
        self.user_id = user_id

    def add_rating(self, rating):
        self.rating = str(ast.literal_eval(self.rating).append(rating))

    def get_rating(self):
        rating = ast.literal_eval(self.rating)
        total = sum(rating)
        count = len(rating)
        rating = total/count

