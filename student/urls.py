from django.urls import path
from .views import Register, Login, Profile, RateTutor
from .views import WishList, Cart, CourseView, AllCourses
from .views import FavCourseLike, FavCourseAll, RateCourse

urlpatterns = [
    path('cart/', Cart.as_view()),
    path('login/', Login.as_view()),
    path('profile/', Profile.as_view()),
    path('register/', Register.as_view()),
    path('wishlist/', WishList.as_view()),
    path('course/all/', AllCourses.as_view()),
    path('course/<int:pk>/', CourseView.as_view()),
    path('course/like/all', FavCourseAll.as_view()),
    path('course/<int:pk>/like', FavCourseLike.as_view()),
    path('course/<int:pk>/rating', RateCourse.as_view()),
    path('tutor/<int:pk>/rating', RateTutor.as_view()),

]
