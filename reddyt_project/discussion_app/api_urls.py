from django.urls import path
from . import api_views

# explanation of urlpatterns down below
urlpatterns = [
    path("vote/", api_views.VoteHandler.as_view(), name="vote_handler"),
]
