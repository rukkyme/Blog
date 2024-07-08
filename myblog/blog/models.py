from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.
'''This class inherits froms Django's models.manager. the manager throughe
which database query operations are provided. instead of using the default manager
which is object, it uses a custom manager which is "published"
'''
class PublishedManager(models.Manager): 
        def get_queryset(self): # This defines a function that will query the database. The method returns a queryset of all objects in the database for that model
            # the super() calls the parent class(models.manager) and used its method 'get_queryset()
            # The filter()method is called on queryset to include only pupblished post.
            return (super().get_queryset().filter(status=Post.Status.PUBLISHED))

        
class Post(models.Model):
    #Status helps to keep track of the condition of a post. is it in draft or is it published
    #We add a status field to each post to store whether it’s a draft or published.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250) # this is a short label that you see in blogs
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', default=1  )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #status field is to save posts as draft before actual publication of posts
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    #the default manager
    objects = models.Manager()
    #the custom manager
    published = PublishedManager()

    #class meta holds extra information about how the model
    class Meta: 
        #hypen before field name is to indicate 
        #a descending order for the date of publishing.such that post are returned in reverse. (ie the last one on top)
        ordering = ['-publish']
        #Indexes help the database find and sort information faster. They are like an extra table of 
        #contents in a book. indexes option in the Meta class, tell Django to create these helpful 
        #table of contents" for your data. it can be one or more field, but in this case it the publish field
        indexes = [models.Index(fields=['-publish']),]
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
        
    
        
        
    def __str__(self):
        return self.title, self.slug
