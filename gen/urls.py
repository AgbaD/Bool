from django.urls import path
from .views import CourseView, CategoryAll, AllCourses
from .views import CategoryCourses, TutorView, TutorCourse, AllTutors

urlpatterns = [
    path('tutor/<int:pk>/courses', TutorCourse.as_view()),
    path('category/courses/', CategoryCourses.as_view()),
    path('course/<int:pk>/', CourseView.as_view()),
    path('category/all/', CategoryAll.as_view()),
    path('tutor/<int:pk>/', TutorView.as_view()),
    path('course/all/', AllCourses.as_view()),
    path('tutor/all/', AllTutors.as_view()),
]
