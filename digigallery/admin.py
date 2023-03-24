from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


def make_published(modeladmin, request, queryset):
    """
    This allows for easy/mass updating of posts in our admin panel.
    It adds an option to our admin dropdown with the following function.

    Arguments:
    - modeladmin: the ModelAdmin instance that's invoking this action
    - request: the current HTTP request object
    - queryset: a QuerySet containing all selected posts

    """
    queryset.update(status=1)


# description to be displayed as the name of the action in the admin interface
make_published.short_description = "Mark selected posts as published"


# original walkthrough project code with changes for new format of models
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    actions = [make_published]
    summernote_fields = ('prompt', 'negprompt', 'method')
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'prompt', 'negprompt', 'method']
    list_filter = ('status', 'created_on')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    actions = ['approve_comments']
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'body')

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
