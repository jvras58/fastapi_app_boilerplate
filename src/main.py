"""Main module of the application."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from communs.message_schema import MessageSchema
from config.settings import get_settings


@asynccontextmanager
async def life_span(app: FastAPI) -> any:  # noqa: ARG001
    """Load and clean up restaurantes data."""
    print('Starting application')
    print('Loading settings')
    print(get_settings().model_dump)
    yield
    print('Shooting down application')


app = FastAPI(lifespan=life_span)


origins = ['http://localhost', 'http://localhost:8888']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=status.HTTP_200_OK, response_model=MessageSchema)
def get_root() -> MessageSchema:
    """Método GET para a ROOT da API."""
    return MessageSchema(
        id=1,
        type='success',
        sumary='API is running',
        message='API is running',
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8888, reload=True)
