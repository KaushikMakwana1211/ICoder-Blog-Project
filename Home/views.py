from django.shortcuts import render, HttpResponse, redirect
from Home.models import Contact
from django.contrib import messages
from Blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# HTML Pages
def home(request):
    # Fetch top three posts based on number of views
    context = {}
    return render(request, "Home/home.html", context)


def about(request):
    return render(request, "Home/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        content = request.POST["content"]
        print(name, email, phone, content)

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfuly sent")
    return render(request, "Home/contact.html")


def search(request):
    query = request.GET["query"]
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, "No search result found. Please refine your query")

    param = {"allPosts": allPosts, "query": query}
    return render(request, "Home/search.html", param)


# Authentication APIs
def handaleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # Checks for errorneous inputs
        # Username must be under 10 characters
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect("home")

        # Username must be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect("home")

        # Password should match
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect("home")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been created")
        return redirect("home")
    else:
        return HttpResponse("404 - Not Found")


def handaleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST["loginusername"]
        loginpass = request.POST["loginpass"]

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect("home")

    return HttpResponse("404 - Not Found")


def handaleLogout(request):
    logout(request)
    messages.success(request, "Sucessfully Logged Out")
    return redirect("home")
