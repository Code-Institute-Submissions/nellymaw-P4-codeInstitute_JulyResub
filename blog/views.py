from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import Post

# Create your views here.

class PostList(ListView):
    model = Post
    queryset = Post.objects.order_by("-created_on")
    template_name = "posts_list.html"
    paginate_by = 3
    
class PostDetail(View):
    
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
            },
        )