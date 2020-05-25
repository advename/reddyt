from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # add this line
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from notification_app.models import Notification


def mark_as_read_and_redir(request, notif_id):
    notification = get_object_or_404(Notification, id=notif_id)
    notification.read = True
    notification.save()
    return HttpResponseRedirect(reverse("discussion_app:single_post",  kwargs={"post_id": notification.post.id}) + "?notif_ref=true")
