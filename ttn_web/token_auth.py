from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_key):
    return Token.objects.get(key=token_key).user


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict((x.split('=') for x in scope['query_string'].decode().split("&")))
        token = query['token']
        scope['user'] = await get_user(token)
        print(scope['user'])
        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
