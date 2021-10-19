from rest_framework import serializers
from .models import Tutor, Course, CourseFiles


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'firstname', 'lastname', 'email']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'tags', 'price', 'tutor']


class CourseFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFiles
        fields = '__all__'
