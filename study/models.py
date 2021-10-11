from django.db import models
import ast

# Create your models here.


class Student(models.Model):
    firstname = models.CharField(max_length=103)
    lastname = models.CharField(max_length=103)
    email = models.EmailField("stud@lms.com")
    course_id = models.CharField('', max_length=1301)
    user_id = models.IntegerField(default=0)

    def add_course_id(self, x):     # x is course id: int
        b = ast.literal_eval(self.course_id)
        b.append(str(x))
        self.course_id = str(b)

    def get_course_ids(self):
        c = ast.literal_eval(self.course_id)
        return c

    def remove_course_id(self, y):  # y is course id: int
        d = ast.literal_eval(self.course_id)
        d.remove(str(y))
        self.course_id = str(d)