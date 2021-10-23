from django.http import Http404
from student.models import Student
from tutor.models import Course, Tutor
from student.serializer import StudentSerializer
from tutor.serializer import CourseSerializer, TutorSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.


class Ping(APIView):

    def get(self, request):
        return Response({'details': 'You are Connected'}, status=status.HTTP_200_OK)


class CourseView(APIView):

    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryAll(APIView):

    def get(self, request):
        try:
            categories = Course.objects.order_by().values('category').distinct()
        except Course.DoesNotExist:
            raise Http404
        return Response(list(categories), status=status.HTTP_200_OK)


class CategoryCourses(APIView):

    def get(self, request, category):
        try:
            courses = Course.objects.filter(category=category)
        except Course.DoesNotExist:
            raise Http404
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TutorView(APIView):

    def get(self, request, pk):
        try:
            tutor = Tutor.objects.get(pk=pk)
        except Tutor.DoesNotExist:
            raise Http404
        serializer = TutorSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TutorCourse(APIView):

    # tutor public key
    def get(self, request, pk):
        try:
            tutor = Tutor.objects.get(pk=pk)
        except Tutor.DoesNotExist:
            raise Http404
        courses = tutor.course_set.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllCourses(APIView):

    def get(self, request):
        try:
            courses = Course.objects.all()
        except Course.DoesNotExist:
            raise Http404
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllTutors(APIView):

    def get(self, request):
        try:
            tutors = Tutor.objects.all()
        except Tutor.DoesNotExist:
            raise Http404
        serializer = TutorSerializer(tutors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)