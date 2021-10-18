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


class Course(models.Model):
    title = models.CharField("Title", max_length=300)
    description = models.TextField("description")
    category = models.CharField("category", max_length=50)
    tags = models.CharField("tags", max_length=130)     # list of tags
    price = models.FloatField(default=0.0)
    tutor = models.CharField("", max_length=200)
    tutor_id = models.IntegerField(default=0)
    public_id = models.CharField(default=str(uuid.uuid4()), max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0)
    rating = models.CharField("[]", max_length=1300)  # a list of rating. Return mean of values
    # dict containing links to google drive containing each file
    # module number as key and course files object as value
    files = models.TextField("Course files")
    students = models.TextField("List of student ids")

    def add_tag(self, tag):
        self.tags = str(ast.literal_eval(self.tags).append(tag))

    def remove_tag(self, tag):
        self.tags = str(ast.literal_eval(self.tags).remove(tag))

    def get_tags(self):
        return ast.literal_eval(self.tags)

    def add_discount(self, percentage):
        self.discount = True
        try:
            self.discount_percentage = percentage
        except Exception as e:
            return e

    def remove_discount(self):
        self.discount = False
        self.discount_percentage = 0

    def add_files(self, module, file_object):
        files = ast.literal_eval(self.files)
        files[module] = file_object
        self.files = str(files)

    def remove_files(self, module):
        files = ast.literal_eval(self.files)
        del(files[module])
        self.files = str(files)

    def add_rating(self, rating):
        self.rating = str(ast.literal_eval(self.rating).append(rating))

    def get_rating(self):
        rating = ast.literal_eval(self.rating)
        total, count = sum(rating), len(rating)
        return round(total/count, 1)


class CourseFiles(models.Model):
    course_id = models.IntegerField(default=0)
    module = models.IntegerField(default=0)
    links = models.CharField("file url", max_length=33)

    def add_link(self, link):
        self.links = str(ast.literal_eval(self.links).append(course_id))

    def remove_course(self, course_id):
        self.courses = str(ast.literal_eval(self.courses).remove(course_id))

    def get_courses(self):
        return ast.literal_eval(self.courses)
