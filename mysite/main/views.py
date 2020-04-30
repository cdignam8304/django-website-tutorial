from django.shortcuts import render, redirect # to render a template and redirect to another template
from django.http import HttpResponse # to render raw HTML
from .models import Tutorial, TutorialCategory, TutorialSeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def single_slug(request, single_slug):
    """"
        Determine whether single_slug relates to a Category or a Tutorial
        Params:
            - single_slug: e.g. in  "localhost:8000/admin/", admin is the single_slug
    """
    # print("The function single_slug has been called...") # for debug
    # print(f"The single_slug is: {single_slug}") # for debug
    
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    if single_slug in categories:
        
        # Get the series that relate to the category that was selected:
        matching_series = TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        
        # Find the tutorials that are part 1s from the matching series and
        # store each matching series object and the first tutorial of each series in a dict:
        series_urls = {}
        for m in matching_series.all():
            part_one = Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series).earliest("tutorial_published")
            series_urls[m] = part_one.tutorial_slug
        
        return render(request=request,
                      template_name="main/category.html",
                      context={"part_ones": series_urls})  
    
    tutorials = [t.tutorial_slug for t in Tutorial.objects.all()]
    if single_slug in tutorials:
        this_tutorial = Tutorial.objects.get(tutorial_slug=single_slug) # get returns an object. filter returns a list.
        tutorials_from_series = Tutorial.objects.filter(tutorial_series__tutorial_series=this_tutorial.tutorial_series).order_by("tutorial_published")
        this_tutorial_idx = list(tutorials_from_series).index(this_tutorial) # to highlight current tutorial in sidebar
        
        return render(request=request,
                      template_name="main/tutorial.html",
                      context={"tutorial": this_tutorial,
                               "sidebar": tutorials_from_series,
                               "this_tutorial_idx": this_tutorial_idx})
    
    return HttpResponse(f"{single_slug} is not a category or a tutorial!!!")


# Create your views here.

def homepage(request):
     
     return render(request=request, # to be able to reference things like user details etc
                   template_name="main/categories.html", # where to find the template to be rendered
                   context={"categories": TutorialCategory.objects.all}) # tutorials is variable name passed to template


def register(request): # NB: The default request is a GET request
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid(): # check the form filled out correctly
            user = form.save() # commit the new user record to the database
            username = form.cleaned_data.get("username") # django has some built-in field preprocessing
            messages.success(request, f"New Account Created: {username}") # creates, but does not display the message
            login(request=request, user=user) # so new user doesn't have to login again afer registering
            messages.info(request, f"You are now logged in as: {username}")
            return redirect("main:homepage") # arg using the variable names created in urls.py in main
        else:
            # Implement a short-term error handling solution:
            for msg in form.error_messages: # form.error_messages is a dict
                # print(form.error_messages[msg]) # prints errors to console
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request=request, # This handles the default GET request
                  template_name="main/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    
    if request.method == "POST":
        form = AuthenticationForm(request=request,
                                  data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as: {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


def new_tabs(request):
    categories = [c.category_slug for c in TutorialCategory.objects.all()]
    
    if request.user.is_authenticated:
        return render(request=request,
                      template_name="main/newtabs.html",
                      context={"categories": categories})
    
    return redirect("main:login") # if user not authenticated, go to login screen
    