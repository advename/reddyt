from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from discussion_app.models import Vote, Post


# Handle votes (upvote, downvote or updating the vote)
class VoteSerializer(serializers.ModelSerializer):

    # Django expects an post_id to lookup the relative post, and returns a post instance
    # Here, we can use an alias to make the field more clear what we expect
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(),
                                                 source='post',
                                                 write_only=True)

    class Meta:
        model = Vote
        fields = (
            'vote', 'post_id'
        )  # we retrieve the logged in user ourself, no need to provide it

    def create(self, validated_data):
        val_user = None
        # !!! in order to access request, we have to provide it in our view file!!!!
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            val_user = request.user
        val_vote = self.validated_data['vote']
        val_post = self.validated_data['post']
        vote, created = Vote.objects.update_or_create(
            user=val_user, post=val_post, defaults={"vote": val_vote})
        return vote

    def update(self, instance, validated_data):
        val_user = None
        # !!! in order to access request, we have to provide it in our view file!!!!
        request = instance.context.get("request")
        if request and hasattr(request, "user"):
            val_user = request.user
        val_vote = instance.validated_data['vote']
        val_post = instance.validated_data['post']
        vote, created = Vote.objects.update_or_create(
            user=val_user, post=val_post, defaults={"vote": val_vote})
        return instance