from .models import Comment, Post
from django import forms
# Imports slugify and ValidationError utilities
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# Import the cloudinary module and its uploader sub-module
import cloudinary
import cloudinary.uploader


# original walkthrough project code
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


# new custom code for P4
class SubmitForm(forms.ModelForm):
    """

    - Inherits from djangos ModelForm class - allows submission
    with image required

    - Our image is uploaded using a custom field type provided
    by the 'django-cloudinary-storage' library. When called it
    use the CloudinaryField to handle image submission to the
    service. It saves then returns a URL to the Post model so it
    can be accessed later.

    - overrides the detault form behaviour for author, allowing
    the author field to be prepopulated rather than selected
    from a drop down list.

    - we use the clean method here to allow checking and
    validation of the form data when it is passed.

    - The form checks for unique slug and to see if
    the title is already in use, returns an error when
    appropriate.

    - Finally we override the default save behaviour
    to run final checks and allow for future additions.

    """
    # Meta class specifies which model and fields the form uses
    class Meta:
        model = Post
        fields = ['title', 'prompt', 'negprompt', 'method', 'featured_image']

    # Additional field for the featured image set to required
    featured_image = forms.ImageField(required=True)

    # Override the default form behaviour as detailed above *
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(SubmitForm, self).__init__(*args, **kwargs)

    # Call clean method to obtain the cleaned data
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title:
            # If title is true Generate a slug from the title
            slug = slugify(title)
            count = 1
            # Append the counter to the slug and increment the counter
            while Post.objects.filter(slug=slug).exists():
                slug = f'{slug}-{count}'
                count += 1
            cleaned_data['slug'] = slug
            # If title already exists, raise a validation error
            if Post.objects.filter(slug=slug).exists():
                raise forms.ValidationError("This title already exists.")
        # Return the cleaned data and slug
        return cleaned_data

    # File size check
    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        # Get image from cleaned data
        if image:
            # If image exceeds 1MB return error
            if image.size > 1000000:
                raise ValidationError('File size exceeds current 1 MB limit.')
        return image

    def save(self, commit=True):
        # Create instance of Post model but don't save yet
        instance = super(SubmitForm, self).save(commit=False)
        # Set the slug to the unique slug generated previously
        self.instance.slug = self.cleaned_data['slug']
        # Set the author to pre-populated author value
        if self.author:
            instance.author = self.author
        if commit:
            instance.save()
        # Commit is run then the instance is saved to the DB
        return instance
