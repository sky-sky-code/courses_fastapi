import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routers import api

import settings

app = FastAPI(description='forms.spnavigator.ru', title='FastAPI forms.spnavigator.ru', version='0.7.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

app.include_router(api.router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
