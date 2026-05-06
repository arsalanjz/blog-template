from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
path('post/<int:post_id>/<str:post_slug>',views.PostDetailView.as_view(),name='detail_post'),
path('post/delete/<int:post_id>/',views.PostDeleteView.as_view(),name='delete_post'),
path('post/create/',views.PostCreateView.as_view(),name='create_post'),
path('post/update/<int:post_id>/',views.PostUpdateView.as_view(),name='update_post'),
]