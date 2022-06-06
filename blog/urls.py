from django.urls import path


from . import views

urlpatterns = [
     path(
          "",
          views.PostList.as_view(),
          name="home"
          ),
     path(
          'posts/<slug:slug>/', 
          views.PostDetail.as_view(), 
          name='post_detail'
          ),
     path(
          'like/<slug:slug>', 
          views.PostLike.as_view(), 
          name='post_like'
          ),
     path("posts/<int:pk>/remove",
          views.DeletePostView.as_view(),
          name="deletepost"),
     ]