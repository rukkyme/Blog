from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
#from django.http import Http404 
from .models import Post
from .forms import EmailPostForm



# Create your views here.
#using Class Based View
class PostListView(ListView):
    #this tells django to use the Post model to retrieve the list of objects
    #by default it will use Post.objects.all to fetch all the records from the table. but then line 16 overides it.
    model = Post
    #This overides the default queryset to use a customized one. it specitfies that only published post shold be fetched
    queryset = Post.published.all()
    #this customize(= posts) the variable name for the list of objects(context_object_name) retrieved from the database 
    #when retrieved, django passes it to template as post for ease of readability.
    context_object_name = 'posts'
    #this enables pagination and limits the number of posts displayed per page to 3
    paginate_by = 3
    #This specifies the template that will be used to render the page
    #it uses post instead of 'blog/object_list/list.html. Thanks to context_object_name, an attribute of django's CBV that inherit form ListView.
    template_name = 'blog/post/list.html'
    

"""
#using function based view.
def post_list(request): 
    #fetch all published posts from the Post model
    post_list = Post.published.all()
    #adding pagination with 3 posts per page
    paginator = Paginator(post_list, 3) 
    #retrievng the GET HTTP parameter and store in page_number variable, if not in Get parameter
    #we use default value 1 to load the first page of results
    page_number = request.GET.get('page', 1)
    #obtain desired page by calling the page() and then we store object in posts.
    try: posts = paginator.page(page_number) 
    except EmptyPage: # If page_number is out of range get last page of results 
        posts = paginator.page(paginator.num_pages)
        #request is the HTTP resquest object that triggers view
    return render(request, 'blog/post/list.html', {'posts' : posts})
"""


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
#the post_detail  takes in year,month,day as parameter to match the URL parameters and retrieve a published post with the given slug 
# and publication date. 
def post_detail(request, year, month, day, post): 
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post' : post})

#function post_share takes in parameter, 1.request(which is an http request object from a user visiting a web page)
#2. post_id(which is the unique ID of the post being shared)
def post_share(request, post_id):
    #this retrieves a Post object from the database, where id equals post_id and get_oject_or_404 gets objects from database if it exists else returns 404
    post = get_object_or_404( Post, id=post_id, status=Post.Status.Published)
    if request.method == 'POST':  #This checks if the request was made using the POST method
        form = EmailPostForm(request.POST) #If the request is a POST, an instance of EmailPostForm (a form class) is created, and the submitted form data (request.POST) is passed into it.
        if form.is_valid():
        #If the form is valid, cleaned_data extracts the validated form data as a dictionary.  
            cd = form.cleaned_data
        else: form = EmailPostForm()
        #This renders an HTML template called 'blog/post/share.html' and sends it back to the user.
        return render( request, 'blog/post/share.html', { 'post': post, 'form': form})