from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from cloudinary import api as cloudinary_api
from .models import Post, Comment
from .forms import CommentForm, SubmitForm
from django.db.models import Count


def toggle_post_status(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    # toggle the status to publish field between 0 and 1
    post.status = 1 - post.status
    post.save()
    messages.success(request, 'The post has been published!')
    return HttpResponseRedirect(reverse('account_posts'))


class PostList(generic.ListView):
    model = Post
    template_name = 'gallery.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=1).order_by('-created_on')


class AuthorPostList(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'account.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            # If the user is a superuser or staff, include all draft posts
            queryset = Post.objects.filter(status=0)
            # Also include posts where the author is the current user
            queryset = queryset | Post.objects.filter(author=user)
        else:
            # Otherwise, only include posts where the author is the current
            queryset = Post.objects.filter(author=user)
        queryset = queryset.order_by('-created_on')
        return queryset


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
            messages.success(request, 'Comment submitted')

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
            messages.warning(request, 'Your like has been removed')
        else:
            post.likes.add(request.user)
            messages.success(request, 'Thanks for the like!')

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
            messages.success(request, 'You have submitted a new post!')
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


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # Delete featured image from Cloudinary
        cloudinary_public_id = post.featured_image.public_id
        if cloudinary_public_id:
            cloudinary_api.delete_resources([cloudinary_public_id])

        # Delete the post once image has been deleted
        post.delete()

        messages.warning(request, 'Your post has been deleted!')
        return redirect('account_posts')


class PostUpdateView(View):
    template_name = 'post_update.html'

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            'post': post
        }
        return render(request, self.template_name, context)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.prompt = request.POST.get('prompt')
        post.negprompt = request.POST.get('negprompt')
        post.method = request.POST.get('method')
        post.save()
        messages.success(request, 'Post Updated!')
        return redirect('account_posts')


class CommentDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if request.user.username == comment.name:
            comment.delete()
            messages.warning(request, 'Comment deleted!')
        else:
            messages.error(request, 'You are not the author!')

        # redirect conditionally based on current page
        current_page = request.GET.get('page')
        if current_page == 'account':
            return redirect('account_posts')
        else:
            return redirect('post_detail', slug=comment.post.slug)
