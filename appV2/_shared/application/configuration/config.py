from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'LegalGuard Rest API'

    db_host: str
    db_user: str
    db_port: int
    db_pass: str
    db_name: str