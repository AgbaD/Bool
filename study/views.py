from .serializers import StudentSerializer
from .schema import validate_student
from .models import Student

from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['POST'])
def create_student(request):
    data = request.data
    data["email"] = data["email"].lower()
    resp = validate_student(data)
    if resp['msg'] != 'success':
        return Response(resp['error'], status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=data["email"], email=data["email"], password=data["password"])
    user_id = user.pk
    data["user_id"] = user_id
    del (data["password"])
    serializer = StudentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_object(pk):
    try:
        return Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise Http404


@api_view(['GET'])
def get_student(request, pk):
    student = get_object(pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)

