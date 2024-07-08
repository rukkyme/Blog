from django.shortcuts import render
from django.http import Http404 
from .models import Post
from django.shortcuts import get_object_or_404, render

# Create your views here.

def post_list(request): 
    #fetch all published posts from the Post model
    posts = Post.published.all()
    #request is the HTTP resquest objet that triggers view
    return render(request, 'blog/post/list.html', {'posts' : posts})

#displays a single post using an id
'''uses a try and exception
def post_detail(request, id):
    try :
        post = Post.published.get(id=id)
    #where the id mentioned does not exist it raises an error
    except Post.DoesNotExist:
        raise Htttp404("No Post found")
    return render(request, 'blog/post/detail.html', {'post' : post})
'''
#using the get_object_or_404 shortcut
def post_detail(request, id): 
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post' : post})