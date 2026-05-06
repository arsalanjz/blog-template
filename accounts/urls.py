from django.urls import path
from accounts import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_user'),
    path('profile/',views.UserProfileView.as_view(), name='profile_user'),
    path('profile/<str:username>',views.UserPublicProfileView.as_view(), name='public_profile_user'),
]