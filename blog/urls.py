from django.urls import path
from .views import PostList, PostDetail, PostLike, DeletePostView, AddPost, EditProfile, UpdatePostView


from . import views

urlpatterns = [
     path(
          "",
          PostList.as_view(),
          name="home"
          ),
     path(
          'posts/<slug:slug>/', 
          PostDetail.as_view(), 
          name='post_detail'
          ),
     path(
          'like/<slug:slug>/', 
          PostLike.as_view(), 
          name='post_like'
          ),
     path(
          "posts/<int:pk>/remove/",
          DeletePostView.as_view(),
          name="deletepost"),
     path(
          "add_post/",
          AddPost,
          name="add_post"),
     path(
          "edit_profile/",
          EditProfile,
          name="edit_profile"
          ),
     path(
          "posts/update/<int:pk>/",
          UpdatePostView.as_view(),
          name="update_post"
          ),
     ]
