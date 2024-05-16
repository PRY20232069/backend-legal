from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse

from appV2._shared.application.configuration.middlewares.token_middleware import TokenMiddleware

class AppMiddleware:

    @staticmethod
    async def handle(request: Request, call_next) -> Response | JSONResponse:
        try:
            TokenMiddleware.handle(request)
            return await call_next(request)
        except Exception as e:
            print('-----------------------')
            if hasattr(e, 'status_code'):
                print(f'ERROR {e.status_code}:')
            print(e)
            print('-----------------------')
            if hasattr(e, 'status_code') and hasattr(e, 'message'):
                content = e.message
                status_code = e.status_code
                return JSONResponse(content=content, status_code=status_code)
            else:
                print('ERROR WITHOUT MESSAGE AND STATUS CODE: Internal Server Error\n-----------------------')
                content = {'message': 'Internal Server Error'}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return JSONResponse(content=content, status_code=status_code)