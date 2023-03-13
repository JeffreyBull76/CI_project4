from . import views
from django.urls import path
from .views import AuthorPostList


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('create_post.html', views.Submission.as_view(), name='create_post'),
    path('account.html', views.AuthorPostList.as_view(), name='account_posts'),
]
