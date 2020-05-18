from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_timestamp']

    def __str__(self):
        return f"{self.title} - {self.user.username} - {self.votes}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_timestamp']

    def __str__(self):
        length = 40
        display = (self.text[:length] +
                   '..') if len(self.text) > length else self.text

        return display


class Vote(models.Model):
    vote = models.BooleanField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        length = 40
        title = (self.post.title[:length] +
                 '..') if len(self.post.title) > length else self.post.title

        return f"{self.user.username} - {title}"

    '''
    During an update, we need to use the previous vote value and
    new vote value. There is no native way to access a previous
    field value, BUT we can store it in a variable, when creating
    and instance of the model (happens also during a Vote.objects.update command).
    To do so, use the default __init__ method, which is called during each
    instance activation, and then use it in the respective function (update in
    our case.)
    '''

    def __init__(self, *args, **kwargs):
        super(Vote, self).__init__(*args, **kwargs)
        self.old_vote = self.vote

    # Override save function to modify the Post data
    def save(self, *args, **kwargs):
        self.update_post_votes()
        super(Vote, self).save(*args, **kwargs)

    def update_post_votes(self):
        # Check if the vote already exists
        if not self.pk:
            # Vote is new
            current_votes = self.post.votes
            changer = 1 if self.vote else -1
            self.post.votes = current_votes + changer
            self.post.save()
        else:
            # Vote exists, update
            if self.old_vote != self.vote:
                # Vote changed, change post vote tracker value
                current_votes = self.post.votes
                changer = 1 if self.vote else -1
                self.post.votes = current_votes + changer
                self.post.save()

    # Updates are triggered with the save() method too, EXCEPT using the Model.objects.update() query.
    # Therefore, avoid using the update() method at all (to be safe). This also goes for signals.

    # The idea is that its not possible to revoke a vote, aka no delete overwriting needed


'''
FYI: This whole setup would also be possible using signals (https://docs.djangoproject.com/en/3.0/ref/signals/),
The code below demonstrates the implementation of it. For it to work, you would have to remove the above
save() and update_post_votes() functions.
'''
#     def update_post_votes(sender, instance, **kwargs):
#         # Check if the vote already exists
#         if not instance.pk:
#             # Vote is new
#             current_votes = instance.post.votes
#             changer = 1 if instance.vote else -1
#             instance.post.votes = current_votes + changer
#             instance.post.save()
#         else:
#             # Vote exists, update
#             if instance.old_vote != instance.vote:
#                 # Vote changed, change post vote tracker value
#                 current_votes = instance.post.votes
#                 changer = 1 if instance.vote else -1
#                 instance.post.votes = current_votes + changer
#                 instance.post.save()

# pre_save.connect(Vote.update_post_votes, sender=Vote)
