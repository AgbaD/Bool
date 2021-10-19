from django.http import Http404
from django.contrib.auth.models import User
from models import Tutor, Course, CourseFiles
from schema import validate_tutor, validate_course
from serializer import TutorSerializer, CourseSerializer, CourseFilesSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.


class Register(APIView):

    def post(self, request):
        data = request.data

        schema = validate_tutor(data)
        if schema['msg'] != 'success':
            return Response(schema['error'], status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({'detail': "Email has already been used"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TutorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.create_user(username=data['email'],
                                            email=data['email'],
                                            password=data['password'],
                                            first_name=data['firstname'],
                                            last_name=data['lastname'])
            Token.objects.create(user=user)
            tutor = Tutor.objects.get(email=data['email'])
            tutor.add_user_id(user.id)
            tutor.save()
            serializer_2 = TutorSerializer(tutor)
            return Response(serializer_2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404

    def get(self, request):
        email = request.user.email
        tutor = self.get_object(email)
        serializer = TutorSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.user.email
        tutor = self.get_object(email)
        serializer = TutorSerializer(tutor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email = request.user.email
        tutor = self.get_object(email)
        tutor.active = False
        tutor.save()
        return Response({'detail': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tutor = Tutor.objects.get(email=user['email'])
        if not tutor.active:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'detail': 'Login successful',
            'token': token.key
        })


class EnrolledCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404
        ec = tutor.get_enrolled_courses()
        return Response(ec, status=status.HTTP_200_OK)


class TopCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404
        ec = tutor.get_enrolled_courses()

        tc = {}
        for k, v in ec.items():
            if len(tc) < 3:
                tc[k] = v

        for k, v in ec.items():
            for o, p in tc.items():
                if v > p:
                    del(tc[o])
                    tc[k] = v
                    break

        return Response(tc, status=status.HTTP_200_OK)


class TutorRating(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404

    def get(self, request):
        email = request.user.email
        tutor = self.get_object(email=email)
        return Response({'rating': tutor.get_rating()}, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.user.email
        tutor = self.get_object(email=email)
        tutor.add_rating(request.data['rating'])
        tutor.save()
        return Response({'rating': tutor.get_rating()}, status=status.HTTP_200_OK)


class AllCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        tutor = Tutor.objects.get(email=email)
        courses = Course.objects.filter(tutor=tutor)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.user.email
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404
        data = request.data
        schema = validate_course(data)
        if schema['msg'] != 'success':
            return Response(schema['error'], status=status.HTTP_400_BAD_REQUEST)

        data['tutor'] = tutor
        serializer = CourseSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # pk is course primary key
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseDiscount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # pk is course primary key
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Http404

    def put(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        discount = data['percentage']
        course.add_discount(discount)
        course.save()
        return Response({'detail': 'Discount added'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        course.remove_discount()
        course.save()
        return Response({'detail': 'Discount removed'}, status=status.HTTP_200_OK)


class CourseRating(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # pk is course primary key
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Http404

    def get(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'rating': course.get_rating()}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course = self.get_object(pk)
        tutor = Tutor.objects.get(email=request.user.email)
        if course.tutor != tutor:
            return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        course.add_rating(request.data['rating'])
        course.save()
        return Response({'rating': course.get_rating()}, status=status.HTTP_200_OK)


class CourseFilesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # pk is course primary key
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Http404

    def post(self, request, pk):
        """
            {
                1: ["url1", ...],
                2: [...],
                ...
            }
        """
        course = self.get_object(pk)
        for k, v in request.data:
            cf = CourseFiles(
                course=course,
                module=k
            )
            cf.save()
            for link in v:
                cf.add_link(link)
            cf.save()
        return Response({'details': 'OK'}, status=status.HTTP_200_OK)

    def get(self, request, pk):
        course = self.get_object(pk)
        files = CourseFiles.objects.filter(course=course)
        serializer = CourseFilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



