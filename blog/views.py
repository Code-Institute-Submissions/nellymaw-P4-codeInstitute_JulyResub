from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, View, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.contrib import messages


from .models import Post, Profile
from .forms import ProfileForm, PostForm, CommentForm

# Create your views here.


class PostList(ListView):

    """
    A view to show 3 lastest posts ordered by created
    Args:
        ListView: class based view
    Returns:
        Render of home page with context
    """

    model = Post
    queryset = Post.objects.order_by("-created_on")
    template_name = "posts_list.html"
    paginate_by = 3


class PostDetail(View):

    """
    A view to show individual post, detail
    Update the variables, whether the user has voted and if they have upvoted
    Args:
        PostDetail: class based view
    Returns:
        Render of post detail with context
    """

    def get(self, request, pk, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, pk=pk)
        comments = post.comment_post.order_by("created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, pk, *args, **kwargs):
        queryset = Post.objects
        post = get_object_or_404(queryset, pk=pk)
        comments = post.comment_post.order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": comment_form,
                "liked": liked
            },
        )


class PostLike(LoginRequiredMixin, View):
    """
    A view to show individual post, detail
    Update the variables, whether the user has voted and if they have upvoted
    Args:
        PostView: class based view
    Returns:
        Return a True or False depending on whether the user has liked the post
    """

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[pk]))


class DeletePostView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    A view to delete a post
    Args:
        SuccessMessageMixin: SuccessMessageMixin (success message attribute)
        DeleteView: class based view
    Returns:
        Render of delete post with success message
    """
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")
    success_message = "Post deleted"
    
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(owner=owner)


@login_required
def AddPost(request):
    """
    A view to add a post, redirects to the post when submitted
    Args:
        request (object): HTTP request object.
    Returns:
        Render of post form with context
    """
    if not request.user.is_authenticated:
        messages.error(
            request, 'Sorry, only logged in users can create a post.')
        return redirect(reverse('home'))
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.pk = request.POST.get('pk')
            post.owner = request.user
            post.user_name = request.user.username
            post.post_image = request.FILES.get("post_image")
            post.owner = request.user
            post.save()
            messages.success(request, 'Post submitted')
            return redirect(reverse("post_detail", args=[post.pk]))
    context = {"form": form, }
    return render(request, "add_post.html", context)


@login_required
def EditProfile(request):
    """
    Update an existing profile
    Args:
        request (object): HTTP request object.
    Returns:
        Render of profile edit page
    """
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'edit_profile.html', context)


class UpdatePostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    A view to edit a post
    Args:
        SuccessMessageMixin: SuccessMessageMixin (success message attribute)
        UpdateView: class based view
    Returns:
        Render of update post with success message
    """
    model = Post
    form_class = PostForm
    template_name = "update_post.html"
    success_message = "Post updated"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(owner=owner)


def error_404_view(request, exception):
    """
    A view to render 404 error page if the user goes to a non-exist url
    Args:
        request (object): HTTP request object.
        exception: exception error
    Returns:
        Render 404error page
    """
    return render(request, 'error404.html', status=404)


def error_500_view(request):
    """
    A view to render 500 error page if there is a server error
    Args:
        request (object): HTTP request object.
    Returns:
        Render 500error page
    """
    return render(request, 'error500.html', status=500)
