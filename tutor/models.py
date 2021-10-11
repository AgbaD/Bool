from django.db import models
import ast

# Create your models here.


class Tutor(models.Model):
    firstName = models.CharField(max_length=13)
    lastName = models.CharField(max_length=13)
    email = models.EmailField("me@lms.org")
    course_id = models.CharField('', max_length=130)
    user_id = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    joined_date = models.DateField(auto_now_add=True)

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

    def update_rating(self, x):
        if isinstance(x, float):
            self.rating = x



