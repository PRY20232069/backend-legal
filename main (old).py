import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from appV1.models.base.base_entity import Base
from appV1.repositories.configuration.database import engine
from appV1.controllers.users_controller import users_router
from appV1.controllers.profiles_controller import profiles_router
from appV1.controllers.banks_controller import banks_router
from appV1.controllers.contracts_controller import contracts_router
from appV1.controllers.terms_controller import terms_router
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

app.include_router(users_router)
app.include_router(profiles_router)
app.include_router(banks_router)
app.include_router(contracts_router)
app.include_router(terms_router)

@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)