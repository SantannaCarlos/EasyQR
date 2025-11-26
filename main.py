from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.routes import router
from app.database.database import engine, Base
from app.models.invite import Invite

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="EasyQR API",
    description="Sistema de convites com QR Code",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", tags=["QR Code"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("templates/login.html")


@app.get("/login")
async def login_page():
    return FileResponse("templates/login.html")


@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("templates/dashboard.html")


@app.get("/create")
async def create_page():
    return FileResponse("templates/create.html")


@app.get("/validate")
async def validate_page():
    return FileResponse("templates/validate.html")


@app.get("/list")
async def list_page():
    return FileResponse("templates/list.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
