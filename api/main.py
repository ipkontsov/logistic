from fastapi import FastAPI
from api.modules.users.router import router as user_router

app = FastAPI(
    title='Dispatch API',
    description='API для управления распределением водителей'
)

app.include_router(user_router)