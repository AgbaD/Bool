from django.urls import path
from views import Register, Profile, Login
from views import EnrolledCourses, TopCourses, AllCourses

urlpatterns = [
    path('login/', Login.as_view()),
    path('register/', Register.as_view()),
    path('courses/top/', TopCourses.as_view()),
    path('courses/all/', AllCourses.as_view()),
    path('profile/<int:pk>/', Profile.as_view()),
    path('courses/enrolled/', EnrolledCourses.as_view()),

]
