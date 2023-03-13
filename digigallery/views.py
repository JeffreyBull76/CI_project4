from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm, SubmitForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'gallery.html'


class AuthorPostList(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'account.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user).order_by('-created_on')  # noqa


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'image_post.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            comment_form = CommentForm()
        else:
            comment_form = CommentForm()

        context = {
            "post": post,
            "comments": comments,
            "liked": liked,
            "comment_form": comment_form,
        }

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class Submission(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects
        return render(
            request,
            'create_post.html',
            {
                "submit_form": SubmitForm(),
            }
        )

    def post(self, request, *args, **kwargs):
        queryset = Post.objects
        submit_form = SubmitForm(request.POST, request.FILES, author=request.user)  # noqa

        if submit_form.is_valid():
            new_post = submit_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('home')
        else:
            return render(
                request,
                'create_post.html',
                {
                    "submit_form": submit_form,
                    "posted": True,
                },
            )
