from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def contact(request):
    if request.method =='POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        content = request.POST.get('content', '')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly.")
        else:
            messages.success(request, "Your Message has been successfully sent.")
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()

    return render(request, 'home/contact.html')

def about(request):
    messages.success(request, 'this is about')
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    allPostsTitle = Post.objects.filter(title__icontains=query)
    allPostsContent = Post.objects.filter(content__icontains=query)
    allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No Search results found! Please search the query correctly.")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for error inputs
        if len(username) > 10:
            messages.error(request, 'Username must be less then 10 characters')
            return redirect('home') 
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and number.')
            return redirect('home') 
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match please check it again.')
            return redirect('home')
        
        #create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'You iCoder Account has been successfully created.')
        return redirect('home')
    else:
        return HttpResponse('404 page not found.')


def handleLogin(request):
     if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged in')
            return redirect('home')
        else:
            messages.error(request,"Invalid Request, Please try again with correct username and password.")
            return redirect('home')
     else:
        return HttpResponse('404 page not found.')
     


def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')