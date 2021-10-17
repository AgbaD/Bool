from django.urls import path
from views import Register, Profile, CustomAuthToken
from views import EnrolledCourses, TopCourses, AllCourses

urlpatterns = [
    path('register/', Register.as_view()),
    path('profile/<int:pk>/', Profile.as_view()),
    path('login/', CustomAuthToken.as_view()),
    path('courses/enrolled/', EnrolledCourses.as_view()),
    path('courses/top/', TopCourses.as_view()),
    path('courses/all/', AllCourses.as_view()),
]
