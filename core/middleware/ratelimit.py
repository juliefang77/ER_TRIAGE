from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get settings from Django settings
        self.rate_limit = getattr(settings, 'RATE_LIMIT', {
            'DEFAULT': {'requests': 1000, 'window': 3600}
        })['DEFAULT']

    def __call__(self, request):
        # Skip non-API requests
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        # Get client IP
        ip = self.get_client_ip(request)
        
        # Use same limits for everyone
        key = f'ratelimit:{ip}:{request.path}'
        max_requests = self.rate_limit['requests']
        window = self.rate_limit['window']

        try:
            request_count = cache.get(key, 0)
            
            if request_count >= max_requests:
                return JsonResponse({
                    'error': '请求过于频繁，请稍后再试',
                    'retry_after': cache.ttl(key)
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

            # Increment the counter
            if request_count == 0:
                cache.set(key, 1, window)
            else:
                cache.incr(key)

            response = self.get_response(request)
            
            # Add rate limit headers
            response['X-RateLimit-Limit'] = str(max_requests)
            response['X-RateLimit-Remaining'] = str(max_requests - request_count - 1)
            response['X-RateLimit-Reset'] = str(int(time.time() + cache.ttl(key)))
            
            return response

        except Exception as e:
            # Log the error but don't block the request if Redis is down
            print(f"Rate limiting error: {str(e)}")
            return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')