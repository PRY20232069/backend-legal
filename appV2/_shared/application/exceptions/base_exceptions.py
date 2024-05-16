from fastapi import status

class BaseError(Exception):
    message: str = 'Server Internal Error'
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    title: str = 'Internal Server Error'

    def __str__(self):
        return self.message

    def get_response_model(self):
        return {
            "description": self.title,
            "content": {
                "application/json": {
                    "example": self.message
                },
            },
        }

    def get_response_model_array(self, values: list[str]):
        example = [ self.message ] + values
        return {
            "description": f'{self.title} (Different Cases)',
            "content": {
                "application/json": {
                    "example": example
                },
            },
        }


class BaseNotFoundError(BaseError):
    message: str = 'Entity Not Found'
    status_code: int = status.HTTP_404_NOT_FOUND
    title: str = 'Not Found'


class BaseBadRequestError(BaseError):
    message: str = 'Bad Request'
    status_code: int = status.HTTP_400_BAD_REQUEST
    title: str = 'Bad Request'


class BaseUnauthorizedError(BaseError):
    message: str = 'Unauthorized'
    status_code: int = status.HTTP_401_UNAUTHORIZED
    title: str = 'Unauthorized'


class BaseForbiddenError(BaseError):
    message: str = 'Forbidden'
    status_code: int = status.HTTP_403_FORBIDDEN
    title: str = 'Forbidden'


class BaseConflictError(BaseError):
    message: str = 'Unauthorized'
    status_code: int = status.HTTP_409_CONFLICT
    title: str = 'Conflict'

class BaseUnprocessableEntityError(BaseError):
    message: str = 'Unprocessable Entity'
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    title: str = 'Unprocessable Entity'