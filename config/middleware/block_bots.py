# config/middleware/block_bots.py

from django.http import HttpResponseForbidden

class BlockBotsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_agents = [
            "MJ12bot",
            "AhrefsBot",
            "SemrushBot",
            "DotBot",
            "Baiduspider",
            "PetalBot",
            "YandexBot",
            "Sogou",
            "python-requests",
            "curl",
            "wget",
        ]

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()

        if any(bot.lower() in user_agent for bot in self.blocked_agents):
            return HttpResponseForbidden("Forbidden: bot blocked.")

        return self.get_response(request)
