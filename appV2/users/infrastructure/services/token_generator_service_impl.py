import jwt
from datetime import datetime, timedelta

from appV2.users.domain.services.token_generator_service import TokenGeneratorService

from settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class TokenGeneratorServiceImpl(TokenGeneratorService):
    
    def generate(self, id: int) -> str:
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"id": id, "exp": expiration}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token