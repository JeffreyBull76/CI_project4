from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# class SubmitForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('author', 'title', 'content', 'slug', 'excerpt',)
