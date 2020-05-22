from rest_framework.views import APIView  # APIView class
from rest_framework.response import Response   # allow to send response
from .models import Notification


class UnreadNotification(APIView):
    # Since isAuthenticated permission class is set globally
    # we do not have to check for if the user is logged in

    def get(self, request, format=None):
        unread_notif = Notification.objects.filter(
            recipient=request.user, read=False).count()
        return Response({
            'unread_notif': unread_notif
        })
