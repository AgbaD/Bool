from models import Tutor
from django.http import Http404
from schema import validate_tutor
from serializer import TutorSerializer
from django.contrib.auth.models import User

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
        if not tutor.active:
            return Http404
        serializer = TutorSerializer(tutor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        email = request.user.email
        tutor = self.get_object(email)
        if not tutor.active:
            return Http404
        serializer = TutorSerializer(tutor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        email = request.user.email
        tutor = self.get_object(email)
        if not tutor.active:
            return Http404
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


class AllCourses(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email
        try:
            tutor = Tutor.objects.get(email=email)
        except Tutor.DoesNotExist:
            return Http404

        courses = tutor.get_courses()
        return Response(courses, status=status.HTTP_200_OK)


