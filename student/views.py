from .models import Student
from django.http import Http404
from .schema import validate_student
from .serializer import StudentSerializer
from django.contrib.auth.models import User
from tutor.models import Course, CourseFiles, Tutor
from tutor.serializer import CourseSerializer, CourseFilesSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.

class Register(APIView):

    # create account
    def post(self, request):
        try:
            data = request.data

            schema = validate_student(data)
            if schema['msg'] != 'success':
                return Response({'details': schema['error']}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=data['email']).exists():
                return Response({'detail': "Email has already been used"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = StudentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.create_user(username=data['email'],
                                                email=data['email'],
                                                password=data['password'],
                                                first_name=data['firstname'],
                                                last_name=data['lastname'])
                Token.objects.create(user=user)
                try:
                    student = Student.objects.get(email=data['email'])
                except Student.DoesNotExist:
                    raise Http404
                student.user_id = user.id
                student.save()
                ser = StudentSerializer(student)
                return Response(ser.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise Http404

    # get profile
    def get(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # edit profile
    def put(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # delete or deactivate profile
    def delete(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            student.active = False
            student.save()
            return Response({'detail': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            password = request.data['password']
            user = request.user
            user.set_password(password)
            user.save()
            return Response({'detail': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            student = Student.objects.get(email=user.email)
        except Student.DoesNotExist:
            raise Http404
        if not student.active:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'detail': 'Login successful',
            'token': token.key
        })


class WishList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise Http404

    # get wishlist
    def get(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            return Response({'wishlist': student.get_wishlist()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # add to wishlist
    def put(self, request):
        try:
            email = request.user.email
            course_id = request.data['course_id']
            student = self.get_object(email)
            student.add_to_wishlist(course_id)
            student.save()
            return Response({'wishlist': student.get_wishlist()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # remove from wishlist

    # clear wishlist
    def delete(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            student.clear_wishlist()
            student.save()
            return Response({'detail': 'Wishlist cleared'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Cart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise Http404

    # get cart
    def get(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            return Response({'cart': student.get_cart()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # add to cart
    def put(self, request):
        try:
            email = request.user.email
            course_id = request.data['course_id']
            student = self.get_object(email)
            student.add_to_cart(course_id)
            student.save()
            return Response({'cart': student.get_cart()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # remove from cart

    # clear cart
    def delete(self, request):
        try:
            email = request.user.email
            student = self.get_object(email)
            student.clear_cart()
            student.save()
            return Response({'detail': 'Cart cleared'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    # get course and course files
    def get(self, request, pk):
        try:
            course = self.get_object(pk)
            email = request.user.email
            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                raise Http404
            courses = student.courses.all()
            if course in courses:
                course_serializer = CourseSerializer(course)
                try:
                    files = CourseFiles.objects.filter(course=course)
                except CourseFiles.DoesNotExist:
                    raise Http404
                file_serializer = CourseFilesSerializer(files, many=True)
                return Response({'course': course_serializer.data, 'files': file_serializer.data},
                                status=status.HTTP_200_OK)
            return Response({'details': 'You are not enrolled for this course'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # pk is course primary key
    # enroll for a course
    def put(self, request, pk):
        try:
            course = self.get_object(pk)
            email = request.user.email
            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                raise Http404
            courses = student.courses.all()
            if course in courses:
                return Response({'detail': 'You are already enrolled to this course'}, status=status.HTTP_200_OK)
            student.courses.add(course)
            tutor = course.tutor
            course_title = course.title
            tutor.add_enrolled_course(course_title)
            tutor.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# all courses a student is enrolled to
class AllCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            email = request.user.email
            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                raise Http404
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavCourseLike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # pk is the course primary key
    # add to fav course i.e like a course
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        if not course:
            raise Http404
        email = request.user.email
        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            raise Http404
        fav_courses = student.fav_courses.all()
        if course in fav_courses:
            return Response({'detail': 'Course liked'}, status=status.HTTP_200_OK)
        student.fav_courses.add(course)
        return Response({'detail': 'Course liked'}, status=status.HTTP_200_OK)


class FavCourseAll(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            email = request.user.email
            try:
                student = Student.objects.get(email=email)
            except Student.DoesNotExist:
                raise Http404
            fav_courses = student.fav_courses.all()
            serializer = CourseSerializer(fav_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RateCourse(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get rating
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        return Response({'rating': course.get_rating()}, status=status.HTTP_200_OK)

    # add rating
    def post(self, request, pk):
        try:
            try:
                course = Course.objects.get(pk=pk)
            except Course.DoesNotExist:
                raise Http404
            rating = request.data['rating']
            course.add_rating(rating)
            course.save()
            return Response({'details': 'Rating Updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RateTutor(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # get rating
    def get(self, request, pk):
        try:
            tutor = Tutor.objects.get(pk=pk)
        except Tutor.DoesNotExist:
            raise Http404
        return Response({'rating': tutor.get_rating()}, status=status.HTTP_200_OK)

    # add rating
    def post(self, request, pk):
        try:
            try:
                tutor = Tutor.objects.get(pk=pk)
            except Tutor.DoesNotExist:
                raise Http404
            rating = request.data['rating']
            if rating > 5:
                return Response({'detail': "Rating should be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

            tutor.add_rating(rating)
            tutor.save()
            return Response({'details': 'Rating Updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": "Error! Something went wrong. We are doing our checks now. Kindly retry and "
                                        "check on your end too"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


