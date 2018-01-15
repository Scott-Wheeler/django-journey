from django.urls import path

from . import views

## /polls/ has been stripped off by the root URLconf

# app_name defines the application namespace
app_name = "polls"

urlpatterns = [
    # /polls/
    path("", views.index, name="index"),

    # /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),

    # /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),

    # /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote")
]