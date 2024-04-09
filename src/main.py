"""Main module of the application."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
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


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8888, reload=True)
