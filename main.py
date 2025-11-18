"""
API FastAPI para geração e leitura de QR Codes.

Esta API permite:
- Gerar QR Codes únicos a partir de strings
- Ler e validar QR Codes de imagens
- Armazenar e consultar convites no banco de dados
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.database.database import engine, Base
from app.models.invite import Invite  # noqa: F401

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar aplicação FastAPI
app = FastAPI(
    title="QR Code API",
    description="API para geração e leitura de QR Codes com validação de convites",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api/v1", tags=["QR Code"])


@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "QR Code API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "generate_qrcode": "POST /api/v1/generate-qrcode",
            "read_qrcode": "POST /api/v1/read-qrcode",
            "get_invite": "GET /api/v1/invites/{invite_code}",
            "list_invites": "GET /api/v1/invites"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
