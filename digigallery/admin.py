from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


def make_published(modeladmin, request, queryset):
    queryset.update(status=1)


make_published.short_description = "Mark selected posts as published"


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
