from django.utils import timezone
from user_agents import parse

class ContentViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the view has a `content_object` attribute
        if hasattr(request, 'content_object'):
            content_object = request.content_object

            # Prevent duplicate views using session
            session_key = f"content_viewed_{content_object.__class__.__name__}_{content_object.id}"
            if not request.session.get(session_key, False):
                # Extract user information
                user = request.user if request.user.is_authenticated else None
                ip_address = request.META.get('REMOTE_ADDR')
                user_agent = request.META.get('HTTP_USER_AGENT')
                referrer = request.META.get('HTTP_REFERER', None)

                # Parse user agent
                ua = parse(user_agent)
                device_type = ua.device.family
                browser = ua.browser.family
                os = ua.os.family

                # Create a ContentView record
                content_object.contentview_set.create(
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    referrer=referrer,
                    device_type=device_type,
                    browser=browser,
                    os=os,
                    viewed_at=timezone.now()
                )

                # Mark as viewed in session
                request.session[session_key] = True

        return response