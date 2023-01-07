"""article_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from finder.views import HomePageView,alfa_request,hello_world,advanced,manage_adv

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view()),
    path("alfa",hello_world, name ="test_alfa"),
    # --------------- advanced search -------------------------
    path("adv",advanced.as_view()),
    path("alfa_adv",manage_adv)

]
