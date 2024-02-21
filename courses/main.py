import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api


app = FastAPI(description='forms.spnavigator.ru', title='FastAPI forms.spnavigator.ru', version='0.7.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(api.router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
