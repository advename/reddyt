from django.db import models
from django.contrib.auth.models import User
from discussion_app.models import Post
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class Notification(models.Model):

    class Meta:
        ordering = ['-created_timestamp']

    # Notification type choices
    COMMENT = 'COMMENT'
    VOTE = 'VOTE'
    NOTIFICATION_CHOICES = (
        (COMMENT, 'commented'),
        (VOTE, 'voted'),
    )

    # Fields
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_recipient")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_sender")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=100, choices=NOTIFICATION_CHOICES, default=COMMENT)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} has {self.get_notification_type_display()} on your post \"{self.post.title}\""

    # Send directly a websocket notification to the user, if they are logged in
    def send_websocket_unread_count(sender, instance, **kwargs):
        print("POOSST SAVEEE")
        # Only send websocket if the notification is new
        # if not instance.pk:
        user_room = f"user-{instance.recipient.id}"
        unread_count = Notification.objects.filter(
            recipient_id=instance.recipient.id, read=False).count()
        # unread_count = 21
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_room,
            {
                # each channel layer needs a type. This type is the consumer method to fire on
                "type": "send_message",
                "unread_count": unread_count,
                "notif_type": instance.get_notification_type_display()
            },
        )

        # instance.post.save()


post_save.connect(Notification.send_websocket_unread_count,
                  sender=Notification)
