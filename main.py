import uvicorn
from fastapi import FastAPI
from models.base.base_entity import Base
from repositories.configuration.database import engine
from controllers.users_controller import users_router
from controllers.profiles_controller import profiles_router
from controllers.banks_controller import banks_router
from controllers.contracts_controller import contracts_router
from controllers.terms_controller import terms_router

app = FastAPI()
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