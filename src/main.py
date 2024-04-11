"""Main module of the application."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def life_span(app: FastAPI) -> any:  # noqa: ARG001
    """Load and clean up restaurantes data."""
    print('Starting application')
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


@app.get('/', status_code=status.HTTP_200_OK)
def get_root() -> dict:
    """Método GET para a ROOT da API."""
    return {'msg': 'Bem Vindo ao ROOT da API'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8888, reload=True)
