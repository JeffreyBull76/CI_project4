from .models import Comment, Post
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import cloudinary
import cloudinary.uploader


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'prompt', 'negprompt', 'method', 'featured_image']

    featured_image = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(SubmitForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title:
            slug = slugify(title)
            if Post.objects.filter(slug=slug).exists():
                raise forms.ValidationError("This title already exists.")
            cleaned_data['slug'] = slugify(title)
        return cleaned_data

    def clean_slug(self):
        slug = slugify(self.cleaned_data['title'])
        count = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f'{slug}-{count}'
            count += 1
        return slug

    def save(self, commit=True):
        instance = super(SubmitForm, self).save(commit=False)
        self.instance.slug = self.cleaned_data['slug']
        if self.author:
            instance.author = self.author
        if commit:
            instance.save()
        return instance
