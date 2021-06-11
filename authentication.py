import jwt
from functools import wraps

from sanic import response
from constants import SECRET_KEY


def authenticate():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            token = getattr(args[0], 'token')
            if not token:
                return response.json({'data': 'Not authenticated'}, status=412)

            # the user is authorized.
            # run the handler method and return the response
            try:
                jwt.decode(token, SECRET_KEY)
            except:
                return response.json({'data': 'Invalid token.'}, status=412)
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator
