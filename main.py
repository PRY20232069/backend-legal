import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from appV2._shared.domain.model.entities.base_entity import Base
from appV2._shared.infrastructure.configuration.database import engine
from appV2._shared.application.configuration.middlewares.app_middleware import AppMiddleware
from appV2.users.interfaces.REST.user_routes import user_router
from appV2.profiles.interfaces.REST.profile_routes import profile_router
from appV2.banks.interfaces.REST.bank_routes import bank_router
from appV2.contracts.interfaces.REST.contract_routes import contract_router
from appV2.contracts.interfaces.REST.term_routes import term_router
from appV2.feedback.interfaces.REST.feedback_routes import feedback_router

from settings import ORIGINS_ALLOWED

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS_ALLOWED,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(bank_router)
app.include_router(contract_router)
app.include_router(term_router)
app.include_router(feedback_router)

@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    return await AppMiddleware.handle(request, call_next)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)