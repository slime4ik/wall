# supermaster/decorators.py
from django_ratelimit.decorators import ratelimit as ratelimit_decorator
from django.http import JsonResponse
from rest_framework import status

def ratelimit(key=None, rate=None, method=None, block=True):
    def decorator(fn):
        # Use ratelimit
        limited_fn = ratelimit_decorator(
            key=key, rate=rate, method=method, block=block
        )(fn)
        
        def _wrapper(request, *args, **kwargs):
            try:
                # Try to do request
                response = limited_fn(request, *args, **kwargs)
                
                # If ratelimit worked - request.limited = True
                if getattr(request, 'limited', False):
                    return JsonResponse(
                        {'detail': 'Too many requests'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
                
                return response
                
            except Exception as e:
                # Catch error with ratelimit worked
                if getattr(request, 'limited', False):
                    return JsonResponse(
                        {'detail': 'Too many requests'},
                        status=status.HTTP_429_TOO_MANY_REQUESTS
                    )
                raise e
                
        return _wrapper
    return decorator