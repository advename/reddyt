'''
    This middleware sets CORS Access-Control-Allow-Headers.
    This middleware is NOT required in order for reddyt to work
    and only serves as an example how to implement a middleware
    and how they work.
'''


class CORSMiddleware:
    # One-time configuration and initialization, ignore this method
    def __init__(self, get_response):
        self.get_response = get_response

    # Modify request and response
    def __call__(self, request):

        # HERE: Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        response["Access-Control-Allow-Headers"] = "Accept, Accept-Encoding, Authorization, Content-Type, Dnt, Origin, User-agent, X-CSRFtoken, X-Requested-With"

        # HERE: Code to be executed for each request/response
        # after the view is called.

        return response
