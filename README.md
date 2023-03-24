# ** THE PROMPTIVERSE**

Site description

[View live website here](https://cip4-digigallery.herokuapp.com/account.html)

![Promptiverse AmIresponsive design]()

## [**Table of Contents**](<#table-of-contents>)

* [**OVERVIEW**](<#overview>)
    * [Design Concept](<#design-concept>)
    * [Site Plan](<#site-plan>)
    * [User Stories](<#user-stories>)
    * [Wireframes](<#wireframes>)
    * [Site Structure](<#site-structure>)
    * [User Experience](<#user-experience>)


* [**SITE FEATURES**](<#site-features>)
    * [Inherited Code](<#inherited-code>)
    * [Depreciated Code](<#depreciated-code>)
    * [](<#>)
    * [](<#>)
    * [](<#>)
    * [](<#>)
    * [](<#>)
    * [](<#>)


* [**ROADMAP**](<#roadmap>)


* [**TECHNOLOGY USED**](<#technology-used>)
    * [](<#>)
    * [](<#>)
    * [](<#>)
    * [](<#>)


* [**TESTING**](<#testing>)
    * [Fixed Bugs](<#fixed-bugs>)
    * [](<#>)
    * [](<#>)
    * [](<#>)
    * [Lessons Learned](<#lessons-learned>)


* [DEPLOYMENT](<#deployment>)
* [CREDITS](<#credits>)
* [ACKNOWLEDGEMENTS](<#acknowledgements>)

--------------------------------------------------------
### OVERVIEW

### Design Concept
### Site Plan
### User Stories
### Wireframes
### Site Structure
### User Experience

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### SITE FEATURES

### Depreciated Code
<details><summary>This first version of a post submission function, which worked but did not correctly gather and pre-populate user details. This in practice allowed users to select from a list to designate author as it was just using the admin data for the item. In retrospect a custom built model could have avoided this (see Lessons Learned) but for the scope of the project the solution was to simply rewrite our submission function (see live code). This allowwed me to add other functionality and security. Note the code presented here was done in a test environment on my previous walkthrough project.</summary>

VIEW:
```class Submission(View):
        def get(self, request, *args, **kwargs):
            queryset = Post.objects

            return render(
                request,
                'submit_post.html',
                {
                    "submit_form": SubmitForm(),
                }
            )
```

FORM:
```class SubmitForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ('author', 'title', 'content', 'slug', 'excerpt',)
```
</details>
    
<details><summary>This Code below presented to show the old SubmitForm function code. Later tidied up and moved into one block (see live code)</summary>

OLD CODE:
```def clean(self):
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
```
</details>

<details><summary></summary></details>

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### ROADMAP

content

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### TECHNOLOGY USED

content

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### TESTING

* BUG NOTES:
* In the old PostList view we had an issue rendering the list correctly. This was fixed by user the super() function. It now populates our gallery correctly.

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### DEPLOYMENT

content

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### CREDITS

content

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### ACKNOWLEDGEMENTS

content

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------