from django.http import Http404
from student.models import Student
from tutor.models import Course, Tutor
from student.serializer import StudentSerializer
from tutor.serializer import CourseSerializer, TutorSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.


class CourseView(APIView):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        if not course:
            return Http404
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryAll(APIView):

    def get(self, request):
        categories = Course.objects.order_by('category').values_list('category', flat=True).distinct('city')
        return Response(list(categories), status=status.HTTP_200_OK)


class CategoryCourses(APIView):

    def get(self, request, category):
        courses = Course.objects.filter(category=category)
        if not courses:
            return Http404
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TutorView(APIView):

    def get(self, request, pk):
        tutor = Tutor.objects.get(pk=pk)
        if not tutor:
            return Http404
        serializer = TutorSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TutorCourse(APIView):

    # tutor public key
    def get(self, request, pk):
        tutor = Tutor.objects.get(pk=pk)
        courses = tutor.course_set.all()
        if not courses:
            return Http404
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllCourses(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllTutors(APIView):

    def get(self, request):
        tutors = Tutor.objects.all()
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
