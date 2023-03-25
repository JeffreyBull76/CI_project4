# **THE PROMPTIVERSE**

Digital gallery to post, rate and share AI art work.

[View live website here](https://cip4-digigallery.herokuapp.com)

![Promptiverse AmIresponsive design](readme/assets/images/AmIresponsive_landing.png)

## [**Table of Contents**](<#table-of-contents>)

* [**OVERVIEW**](<#overview>)
    * [Site Plan](<#site-plan>)
    * [Design Concept](<#design-concept>)
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
### **OVERVIEW**

### **Site Plan**
To showcase my learning for Project 4 on my CI course I decided to create a gallery website. This was going to be based on the very basic skeleton of the walkthrough blog project. I have a keen interest in art and creativity and recently have been blown away by advances in AI art generators. So marrying the that interest with a project seemed a good place to start. 

--------------------------------------------------------

### **Design Concept**
Initially I worked directly from the base walkthrough code to get me started. I have included the DB schema below but have not gone into to much detail as aside from some new fields it remains very similar to the original project models.py file.

<details>
<summary>Schema</summary>

![Promptiverse AmIresponsive design](readme/assets/images/DB_Schema.png)

</details>

It is worth noting (more details in lessons learned) I later realised a slightly different solution would have been cleaner, with the image seperated into its own model.
But for the purposes of the project I worked from this base.

--------------------------------------------------------

### **User Stories**

A comprehensive git project page can be found here with my user stories. 

[Project Board](https://github.com/users/JeffreyBull76/projects/5)

I initially used similar stories to the example project but then added more for my specific site. At all times during production the user and admin roles were kept in mind when it came to implementing new functions and even more asthetic design ideas.

--------------------------------------------------------

### **Wireframes**

<details>
<summary>Wireframe</summary>

![Wireframe](readme/assets/images/promptiverse_wireframe.png)

</details>

I used an online wireframe tool to create my basic layout idea [Fluid UI](https://www.fluidui.com/)

This design stayed mostly intact throughout the process. I did in the end decide to leave the login, signup and logout pages seperate because it felt cleaner in production. I left the wireframe as was to show my initial idea of showing them side by side. 

--------------------------------------------------------

### **Final Design**

* Two fonts were chosen:
    * Julius Sans One: Was used for our headers and decorative text. 
    * Poppins: Was used for the main body text elements to give a little more weight

![Julius Sans One](readme/assets/images/Font1.png)


![Poppins](readme/assets/images/Font2.png)

* Color palette
    * Was done in a muted greyscale with an orange 'pop' color to prevent detracting from the artwork

![Colors](readme/assets/images/ColorPalette.png)

* Overall Thoughts: All design elements were chosen to be somewhat neutral and not make the site too busy.


--------------------------------------------------------

### **User Experience**

The nav bar exists in two versions.

* Logged out

* Logged in

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)

--------------------------------------------------------

### **SITE FEATURES**

### **Depreciated Code**
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

<details><summary>Code for removed comments section on account page</summary>

OLD TEMPLATE CODE:
```<!-- shows all comments by current user and allows them to be deleted -->
  <div class="container-fluid">
    <p>COMMENT LIST:</p>
    <div class="row">
      <!-- comments section displays user feedback -->
      {% for comment in user_comments %}
      <div class="col-lg-3 col-md-4 col-sm-12 col-12">
        <div class="card mb-3" id="comment-card">
          <div class="card-header">
            {{ comment.name }} said on {{ comment.created_on }}:
          </div>
          <div class="card-body">
            <p>{{ comment.body }}</p>
            {% if user.is_authenticated and comment.name == user.username %}
            <a href="{% url 'comment_delete' pk=comment.pk %}?page=account"
              class="btn btn-danger btn-sm float-right">Delete</a>
            {% endif %}
          </div>
        </div>
      </div>
      {% empty %}
      <!-- displays a message when no comments are present -->
      <p>No comments yet.</p>
      {% endfor %}
    </div>
  </div>
```

OLD VIEW CODE (added under AuthorPostList)
```def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_comments = Comment.objects.filter(name=self.request.user.username)
        context['user_comments'] = user_comments
        return context
```

</details>

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **ROADMAP**

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **TECHNOLOGY USED**

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **TESTING**

* BUG NOTES:
* In the old PostList view we had an issue rendering the list correctly. This was fixed by user the super() function. It now populates our gallery correctly.

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **DEPLOYMENT**

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **CREDITS**

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------

### **ACKNOWLEDGEMENTS**

--------------------------------------------------------

### [Contents Menu](<#table-of-contents>)
--------------------------------------------------------