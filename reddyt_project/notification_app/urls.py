from django.urls import path  # path deals with the urls

from . import views  # import all our views functions from the current directory

app_name = "notification_app"

# explanation of urlpatterns down below
urlpatterns = [
    path("post/<int:notif_id>", views.mark_as_read_and_redir,
         name="mark_as_read_and_redir"),
]
