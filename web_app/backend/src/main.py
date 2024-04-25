from fastapi import FastAPI

from .router_app import router

app = FastAPI()

app.include_router(router=router)
