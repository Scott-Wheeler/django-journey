from django.urls import path

from . import views

## /polls/ has been stripped off by the root URLconf

## generic.DetailView expects the primary key to be pk

# app_name defines the application namespace
app_name = "polls"

urlpatterns = [
    # /polls/
    path("", views.IndexView.as_view(), name="index"),

    # /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),

    # /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),

    # /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote")
]