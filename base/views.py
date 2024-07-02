from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Blog, Tag, Message, User
from .forms import BlogForm, UserForm, MyUserCreationForm

# Create your views here

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does not Exits')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            return redirect('home') 

        else:
            messages.error(request, 'Username or passsword does not exits')


    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    form  = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An Error Occurred')

    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    blogs = Blog.objects.filter(
        Q(tag__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    
    tags = Tag.objects.all()[0:5]
    blog_count = blogs.count()


    context = {'blogs':blogs, 'tags':tags, 'blog_count':blog_count}
    return render(request, 'base/home.html', context)


def blog(request, pk):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blog = Blog.objects.get(id=pk)
    blog_messages = blog.message_set.all()
    tag = blog.tag

    participants = blog.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            blog = blog,
            body = request.POST.get('body')
        )
        blog.participants.add(request.user)
        return redirect('blog', pk=blog.id)

    context = {'blog':blog, 'blog_messages':blog_messages, 'participants':participants, 'tag':tag}
    return render(request, 'base/blog.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    tags = Tag.objects.all()
    context = {'user':user, 'blogs':blogs, 'tags':tags}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createBlog(request):
    form = BlogForm()
    tags = Tag.objects.all()
    if request.method == 'POST':
        tag_name = request.POST.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        Blog.objects.create(
            host=request.user,
            tag=tag,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            content=request.POST.get('content')
        )
        return redirect('home')

    context = {'form':form, 'tags':tags}
    return render(request, 'base/blog_form.html', context)

@login_required(login_url='login')
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    tags = Tag.objects.all()
    if request.user != blog.host:
        return HttpResponse("Your are not the Owner")

    if request.method == 'POST':
        tag_name = request.POST.get('tag')
        tag, created = Tag.objects.get_or_create(name=tag_name)
        blog.name = request.POST.get('name')
        blog.tag = tag
        blog.description = request.POST.get('description')
        blog.content = request.POST.get('content')
        blog.save()
        return redirect('home')

    context = {'form' : form, 'tags':tags, 'blog':blog}
    return render(request, 'base/blog_form.html', context)

@login_required(login_url='login')
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.user != blog.host:
        return HttpResponse("Your are not the Owner")

    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':blog})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Your are not the Owner")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user) #request.FILES
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    context = {'form':form}
    return render(request, 'base/update_user.html', context)

def tags(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tags = Tag.objects.filter(name__icontains=q)
    context = {'tags':tags}
    return render(request, 'base/tags.html', context)