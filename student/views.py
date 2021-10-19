from django.http import Http404
from django.contrib.auth.models import User
from models import Student
from schema import validate_student
from serializer import StudentSerializer

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

        schema = validate_student(data)
        if schema['msg'] != 'success':
            return Response({'details': schema['error']}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data['email']).exists():
            return Response({'detail': "Email has already been used"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StudentSerializer(data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.create_user(username=data['email'],
                                            email=data['email'],
                                            password=data['password'],
                                            first_name=data['firstname'],
                                            last_name=data['lastname'])
            Token.objects.create(user=user)
            student = Student.objects.get(email=data['email'])
            student.user_id = user.id
            student.save()
            ser = StudentSerializer(student)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, email):
        try:
            return Student.objects.get(email=email)
        except Student.DoesNotExist:
            return Http404

    def get(self, request):
        email = request.user.email
        student = self.get_object(email)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.user.email
        student = self.get_object(email)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email = request.user.email
        student = self.get_object(email)
        student.active = False
        student.save()
        return Response({'detail': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        student = Student.objects.get(email=user['email'])
        if not student.active:
            return Response({'detail': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'detail': 'Login successful',
            'token': token.key
        })
