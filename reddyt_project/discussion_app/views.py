from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required  # add this line
from asgiref.sync import async_to_sync


import validators

# Create your views here.
from .models import Post, Vote, Comment
from notification_app.models import Notification
from django.contrib.auth.models import User


def index(request):
    posts = Post.objects.all()[:5]
    context = {"posts": posts}
    return render(request, "discussion_app/index.html", context)


def single_post(request, post_id):
    error_message = None
    if 'error_message' in request.session:
        error_message = request.session['error_message']
        del request.session['error_message']
    post = get_object_or_404(Post, id=post_id)
    context = {"post": post, "error_message": error_message}
    return render(request, "discussion_app/single_post.html", context)


def comment_form(request, post_id):
    if request.method == "POST":

        # Check if text is valid
        text = request.POST["text"]
        post_owner = get_object_or_404(User, id=request.POST['post_owner'])
        if not text and len(text) < 10:
            request.session['error_message'] = 'Invalid message'
            return redirect("discussion_app:single_post", post_id=post_id)

        user = request.user
        Notification.objects.create(
            recipient_id=request.POST['post_owner'], sender=user, notification_type=Notification.COMMENT, post_id=post_id)
        Comment.objects.create(text=text, user=user, post_id=post_id)

        return redirect("discussion_app:single_post", post_id=post_id)


def new_post(request):
    # context is used to return error messages
    context = {}
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        user = request.user

        if not title and len(title) < 5:
            context = {"error_message": "Title too short"}

        elif not text and len(text) < 10:
            context = {"error_message": "Text too short"}
        else:
            Post.objects.create(title=title, text=text, user=user)
            return HttpResponseRedirect(reverse('discussion_app:index'))
    return render(request, "discussion_app/new_post.html", context)
