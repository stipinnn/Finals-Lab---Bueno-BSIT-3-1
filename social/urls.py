from django.urls import path
from .views import (
    PostListView, PostDetailView, PostEditView, PostDeleteView,
    CommentDeleteView, ProfileView, ProfileEditView,
    PostLikeView, PostDislikeView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),
    path('post/<int:pk>/like/', PostLikeView.as_view(), name='like-post'),
    path('post/<int:pk>/dislike/', PostDislikeView.as_view(), name='dislike-post'),
]
