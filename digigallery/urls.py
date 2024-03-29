from . import views
from django.urls import path
from .views import AuthorPostList, PostDeleteView, CommentDeleteView


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('create_post.html', views.Submission.as_view(), name='create_post'),
    path('account.html', views.AuthorPostList.as_view(), name='account_posts'),
    # Allows deletion of post associated with slug
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='delete_post'),
    # Allows updating of post associated with slug
    path('<slug:slug>/update/', views.PostUpdateView.as_view(),
         name='post_update'),
    # Gets primary key of comment converts to integer and allows deletion
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(),
         name='comment_delete'),
    # Gets post_id converts to integer and allows status toggle
    path('posts/<int:post_id>/toggle_status/', views.toggle_post_status,
         name='toggle_post_status'),
]
