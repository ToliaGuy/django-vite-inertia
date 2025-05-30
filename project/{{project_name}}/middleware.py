from django.contrib.messages import get_messages
from inertia import share, InertiaResponse


class DataShareMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    @staticmethod
    def collect_messages(request) -> list:
        messages = []
        for msg in get_messages(request):
            message = {
				"message": msg.message,
				"level": msg.level,
				"tags": msg.tags,
				"extra_tags": msg.extra_tags,
				"level_tag": msg.level_tag,
			}
            messages.append(message)
        return messages

    def __call__(self, request):

        response = self.get_response(request)
        if hasattr(response, 'request') and hasattr(response.request, 'inertia'):
            messages = self.collect_messages(request)
            if messages:
                share(request, messages=messages)
                response = InertiaResponse(
                    request,
                    response.component,
                    response.props,
                    response.template_data,
                    response.headers
                )

        return response
