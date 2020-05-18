from django.urls import path  # path deals with the urls

from . import views  # import all our views functions from the current directory
'''
A namespace is recommended because you can have a "index"
view function inside your polls/ app, but also inside in another app. This
helps us to specify the view we want.
'''
app_name = "discussion_app"

# explanation of urlpatterns down below
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>", views.single_post, name="single_post"),
    path("post/<int:post_id>/write-comment",
         views.comment_form,
         name="comment_form"),
    path("new-post/", views.new_post, name="new_post"),

]
