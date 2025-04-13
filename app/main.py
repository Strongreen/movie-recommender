from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from app.database import init_db
from app.routers import users, movies, ratings
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Usuários",
        "description": "👤 Endpoints para criação e listagem de usuários."
    },
    {
        "name": "Filmes",
        "description": "🎬 Endpoints para cadastro e listagem de filmes."
    },
    {
        "name": "Avaliações e Recomendação",
        "description": "⭐ Endpoints para avaliação de filmes e recomendações personalizadas."
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="🎥 API - Sistema de Recomendação de Filmes",
    description="""
    **🎬 API para recomendação de filmes com base em preferências dos usuários.**
     com **filtragem colaborativa** e **filtros por conteúdo**  
    - Criado para o desafio técnico de Engenheiro de Software Pleno da **BISO** 🧠
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.biso.digital/"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(movies.router, prefix="/filmes", tags=["Filmes"])
app.include_router(ratings.router, prefix="/classificacoes", tags=["Avaliações e Recomendação"])

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Por medida de Segurança: Esse erro é interno do servidor. Entre em contato com o Administrador"},
    )
