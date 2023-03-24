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
    """

    Extends Django's generic.ListView, defines model as Post
    and spcifies the template to render the view.

    We use super to customize the behavior of the subclass
    while still maintaining the original behavior of the parent class
    (depreciate bug note see readme file)

    Finally we filter the result by published status and when they
    were created.

    """
    model = Post
    template_name = 'gallery.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status=1).order_by('-created_on')


class AuthorPostList(LoginRequiredMixin, generic.ListView):
    """

    This is a modified version of PostList using similar syntax
    it renders to the account page. It serves two purposes.

    It checks first if the user is a superuser or staff, and if so
    returns objects with a status of zero (denoting draft status)
    it then returns the admin/staff members actual posts as well.

    Else it returns the current users posts only when not denoted
    as staff.

    """
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
    """

    This code remains similar to the P4 walkthrough
    project with minor changes to accomodate the new
    scope of our project.

    """
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
    """

    Again here the code raims largely unchanged from the walkthrough
    as this already served its purpose perfectly.

    """
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
    """

    The GET method returns a form rendered by the
    set template. The form instance "SubmitForm()"
    is passed as the "submit_form" variable.

    The POST method checks if the form is valid
    if so it creates a new post entry in the DB

    If it is not valid it returns an error message
    and sets posted to True preventing the form
    being returned again as blank.

    """
    # Creates our form to be rendered
    def get(self, request, *args, **kwargs):
        queryset = Post.objects
        return render(
            request,
            'create_post.html',
            {
                "submit_form": SubmitForm(),
            }
        )

    # Posts our form data
    def post(self, request, *args, **kwargs):
        queryset = Post.objects
        submit_form = SubmitForm(
            request.POST, request.FILES, author=request.user
            )

        # Checks for valid form data and redirects
        if submit_form.is_valid():
            new_post = submit_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            messages.success(request, 'You have submitted a new post!')
            return redirect('home')
        else:
            # re-renders the existing form for editing
            return render(
                request,
                'create_post.html',
                {
                    "submit_form": submit_form,
                    "posted": True,
                },
            )


class PostDeleteView(LoginRequiredMixin, View):
    """

    Uses the LoginRequiredMixing for security allows
    the deletion of posts and their associated images.

    Gets object from DB based on two parameters
    the slug value and request which gathers the HTTP
    data of the associate object (in this case our
    image)

    In our POST method we set the cloudinary_public_id to
    the value of the associated image on our cloudinary
    service. We then check for the cloudinary_public_id's
    existence and if true and valid we delete it from the
    Cloudinary service using an API call.

    Cascade is already set in our models to remove attached
    comments.

    """
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, author=request.user)

        # Delete featured image from Cloudinary
        cloudinary_public_id = post.featured_image.public_id
        if cloudinary_public_id:
            cloudinary_api.delete_resources([cloudinary_public_id])

        # Delete the post once image has been deleted
        post.delete()

        # Return a message and redirect
        messages.warning(request, 'Your post has been deleted!')
        return redirect('account_posts')


class PostUpdateView(View):
    """

    Allows for updating of existing posts using
    GET and POST methods.

    Renders our existing post infomation to the template
    to allow for updating.

    When the user submits the data it re-submits each
    field with the new data and saves to the DB.

    """
    template_name = 'post_update.html'

    def get(self, request, slug):
        # Gets the blog post with the specified slug
        post = get_object_or_404(Post, slug=slug)
        # Return a dictionary based on the values of post above
        context = {
            'post': post
        }
        # Render the post item to the template
        return render(request, self.template_name, context)

    def post(self, request, slug):
        # Gets the blog post with the specified slug
        post = get_object_or_404(Post, slug=slug)
        # Updates all the allowed update fields
        post.prompt = request.POST.get('prompt')
        post.negprompt = request.POST.get('negprompt')
        post.method = request.POST.get('method')
        # Saves the updated blog post and redirects
        post.save()
        messages.success(request, 'Post Updated!')
        return redirect('account_posts')


class CommentDeleteView(LoginRequiredMixin, View):
    """

    As with previous destructive task uses Mixin
    to check for a logged in user.

    GET method uses the http data and Primary Key
    of the associated comment.

    It then checks if the current user is the same
    as the comment author. It then uses the base
    delete() function to remove the comment from
    the database.

    """
    def get(self, request, pk):
        # Two arguments for our Model and PK
        comment = get_object_or_404(Comment, pk=pk)
        # Validation check for comment Author
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
