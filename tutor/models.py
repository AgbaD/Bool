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
    rating = models.CharField(default="[1]", max_length=1300)  # a list of rating. Return mean of values
    user_id = models.IntegerField(default=1000000)
    # a dict of courses enrolled {course_title: number_of_enrollment}
    enrolled_courses = models.TextField(default="{}")
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.firstname, self.lastname)

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

    def get_rating(self):
        rating = ast.literal_eval(self.rating)
        total, count = sum(rating), len(rating)
        return round(total/count, 1)


class Course(models.Model):
    title = models.CharField("Title", max_length=300)
    description = models.TextField("description")
    category = models.CharField("category", max_length=50)
    tags = models.CharField(default="", max_length=130)
    price = models.FloatField(default=0.0)
    # many courses to one tutor
    tutor = models.ForeignKey(Tutor, blank=True, on_delete=models.CASCADE)
    public_id = models.CharField(default=str(uuid.uuid4()), max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)
    # a list of rating. Return mean of values
    rating = models.CharField(default="[1]", max_length=1300)
    # students = many to many relationship

    class Meta:
        ordering = ['title']

    def __str__(self):
        return "%s" % self.title

    def add_discount(self, percentage):
        self.discount = True
        self.discount_percentage = percentage

    def remove_discount(self):
        self.discount = False
        self.discount_percentage = 0

    def get_rating(self):
        rating = ast.literal_eval(self.rating)
        total, count = sum(rating), len(rating)
        return round(total/count, 1)


class CourseFiles(models.Model):
    # Many course files to one course
    course = models.ForeignKey(Course, blank=True, on_delete=models.CASCADE)
    module = models.IntegerField(default=0)
    links = models.CharField(default="[]", max_length=33)

    def __str__(self):
        return "%s \n Module %s" % (self.course, self.module)

    def add_link(self, links):
        print(ast.literal_eval(self.links))
        if self.links == "[]":
            self.links = str(links)
        else:
            lk = ast.literal_eval(self.links)
            lk.extend(links)
            self.links = lk

    def get_links(self):
        return ast.literal_eval(self.links)



