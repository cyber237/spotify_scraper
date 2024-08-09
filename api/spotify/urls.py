from django.urls import re_path

from .views import PodcastDetailView

urlpatterns = [
    re_path(r"ratings/(?P<uid>[a-zA-Z0-9]{22})/$", PodcastDetailView.as_view()),
]
