from django.contrib import admin
from django.urls import path
from finder.views import HomePageView,alfa_request,hello_world,advanced,manage_adv,hello_world_adv

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view()),
    path("alfa",hello_world, name ="test_alfa"),
    # --------------- advanced search -------------------------
    path("adv",advanced.as_view()),
    path("alfa_adv",manage_adv),
    # advanced details ---
    path("adv_details",hello_world_adv, name = "advanced details")

]
