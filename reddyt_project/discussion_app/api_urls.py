from django.urls import path
from discussion_app import api_views

from rest_framework.urlpatterns import format_suffix_patterns

# explanation of urlpatterns down below
urlpatterns = [
    path("vote/", api_views.VoteHandler.as_view(), name="vote_handler"),
]