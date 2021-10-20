from django.urls import path
from .views import Register, Profile, Login, TutorRating
from .views import EnrolledCourses, TopCourses, AllCourses, CreateCourse
from .views import CourseView, CourseDiscount, CourseRating, CourseFilesView

urlpatterns = [
    path('login/', Login.as_view()),
    path('profile/', Profile.as_view()),
    path('register/', Register.as_view()),
    path('courses/top/', TopCourses.as_view()),
    path('courses/all/', AllCourses.as_view()),
    path('profile/rating/', TutorRating.as_view()),
    path('courses/create/', CreateCourse.as_view()),
    path('courses/<int:pk>/', CourseView.as_view()),    # pk is course primary key
    path('courses/enrolled/', EnrolledCourses.as_view()),
    path('courses/<int:pk>/rating/', CourseRating.as_view()),   # pk is course primary key
    path('courses/<int:pk>/files/', CourseFilesView.as_view()),     # pk is course primary key
    path('courses/<int:pk>/discount/', CourseDiscount.as_view()),   # pk is course primary key

]
