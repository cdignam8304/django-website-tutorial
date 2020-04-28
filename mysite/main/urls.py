"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
from django.contrib import admin

app_name = "main" # used for creating custom urls, so don't have to hard code urls

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("admin/", admin.site.urls), # added admin here due to order urls are checked
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"), # we use logout_request as their is a django method called logout that we already imported!
    path("login/", views.login_request, name="login"), # use login_request for same reason as above
    path("new-tabs/", views.new_tabs, name="newtabs"), # try out materialize tabs functionality
    path("<single_slug>/", views.single_slug, name="single_slug"), # get the single_slug from url (using '<>' syntax) and pass it as a variable to the views.single_slug function
]
