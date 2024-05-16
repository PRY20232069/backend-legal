from fastapi.requests import Request
from utils.jwt_utils import JwtUtils

from appV2._shared.application.exceptions.app_exceptions import TokenInvalidError, TokenExpiredError

class TokenMiddleware:

    @staticmethod
    def handle(request: Request):
        
        token = request.headers.get('Authorization')

        # Si el endpoint necesita un token, se lanza el error automáticamente (no se maneja en este middleware)
        if not token:
            return

        if JwtUtils.is_invalid(token):
            raise TokenInvalidError()

        
        if JwtUtils.is_expired(token):
            raise TokenExpiredError()
            

        try:
            user_id = JwtUtils.get_user_id2(token)
            request.state.user_id = user_id
            print('User id obtained correctly')
        except Exception as e:
            print(e)
            raise TokenInvalidError()
        
    
        