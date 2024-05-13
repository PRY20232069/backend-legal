import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from appV2._shared.domain.model.entities.base_entity import Base
from appV2._shared.infrastructure.configuration.database import engine
from appV2.users.interfaces.REST.user_routes import user_router
from appV2.profiles.interfaces.REST.profile_routes import profile_router
from appV2.banks.interfaces.REST.bank_routes import bank_router

from settings import ORIGIN_ALLOWED_1, ORIGIN_ALLOWED_2, ORIGIN_ALLOWED_3, ORIGIN_ALLOWED_4, ORIGIN_ALLOWED_5, ORIGIN_ALLOWED_6

app = FastAPI()

origins = [ ORIGIN_ALLOWED_1, ORIGIN_ALLOWED_2, ORIGIN_ALLOWED_3, ORIGIN_ALLOWED_4, ORIGIN_ALLOWED_5, ORIGIN_ALLOWED_6 ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(bank_router)

@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)