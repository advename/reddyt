from rest_framework import status  # used to return status code
from rest_framework.views import APIView  # APIView class
from rest_framework.response import Response  # allow to send response

from discussion_app.models import Vote  # import Post Model
from discussion_app.serializers import VoteSerializer  # import Post Serializer


# Create or update vote
class VoteHandler(APIView):

    # post function for POST requests
    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data,
                                    context={'request': request})
        # Validate POST data
        if serializer.is_valid():
            # Save to DB and return success status
            serializer.save()
            return Response(serializer.data)

        # Return Error status if validation failed
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
