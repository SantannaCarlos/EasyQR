"""
Testes para os endpoints da API.
"""
import io
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PIL import Image

from main import app
from app.database.database import Base, get_db
from app.api.qrcode_service import QRCodeService

# Criar banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override da função get_db para usar banco de teste."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAPI:
    """Testes para endpoints da API."""

    def test_root_endpoint(self):
        """Testa endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_health_check(self):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_generate_qrcode(self):
        """Testa geração de QR Code via API."""
        response = client.post(
            "/api/v1/generate-qrcode",
            json={"data": "Test invite data"}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        assert "X-Invite-Code" in response.headers
        assert "X-Invite-ID" in response.headers

        # Verificar que é uma imagem válida
        img = Image.open(io.BytesIO(response.content))
        assert img.format == 'PNG'

    def test_generate_qrcode_empty_data(self):
        """Testa geração de QR Code com dados vazios."""
        response = client.post(
            "/api/v1/generate-qrcode",
            json={"data": ""}
        )

        # Deve aceitar string vazia
        assert response.status_code == 200

    def test_read_qrcode_valid(self):
        """Testa leitura de QR Code válido."""
        # Primeiro, gerar um QR Code
        generate_response = client.post(
            "/api/v1/generate-qrcode",
            json={"data": "Test data for reading"}
        )
        assert generate_response.status_code == 200
        invite_code = generate_response.headers["X-Invite-Code"]

        # Criar arquivo para upload
        files = {
            "file": ("test_qrcode.png", generate_response.content, "image/png")
        }

        # Ler QR Code
        read_response = client.post(
            "/api/v1/read-qrcode",
            files=files
        )

        assert read_response.status_code == 200
        data = read_response.json()
        assert data["success"] is True
        assert data["invite_code"] == invite_code
        assert data["data"] == "Test data for reading"
        assert data["is_validated"] is True

    def test_read_qrcode_invalid_file_type(self):
        """Testa leitura com tipo de arquivo inválido."""
        files = {
            "file": ("test.txt", b"Not an image", "text/plain")
        }

        response = client.post(
            "/api/v1/read-qrcode",
            files=files
        )

        assert response.status_code == 400
        assert "imagem" in response.json()["detail"].lower()

    def test_read_qrcode_no_qrcode(self):
        """Testa leitura de imagem sem QR Code."""
        # Criar imagem em branco
        img = Image.new('RGB', (100, 100), color='white')
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        files = {
            "file": ("blank.png", img_io.read(), "image/png")
        }

        response = client.post(
            "/api/v1/read-qrcode",
            files=files
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "não encontrado" in data["message"].lower()

    def test_get_invite(self):
        """Testa consulta de convite por código."""
        # Criar convite
        generate_response = client.post(
            "/api/v1/generate-qrcode",
            json={"data": "Test invite"}
        )
        invite_code = generate_response.headers["X-Invite-Code"]

        # Consultar convite
        response = client.get(f"/api/v1/invites/{invite_code}")

        assert response.status_code == 200
        data = response.json()
        assert data["invite_code"] == invite_code
        assert data["data"] == "Test invite"
        assert data["is_validated"] is False

    def test_get_invite_not_found(self):
        """Testa consulta de convite inexistente."""
        response = client.get("/api/v1/invites/nonexistent-code")

        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()

    def test_list_invites(self):
        """Testa listagem de convites."""
        # Criar alguns convites
        for i in range(3):
            client.post(
                "/api/v1/generate-qrcode",
                json={"data": f"Test invite {i}"}
            )

        # Listar convites
        response = client.get("/api/v1/invites")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 3

    def test_list_invites_pagination(self):
        """Testa paginação da listagem de convites."""
        response = client.get("/api/v1/invites?skip=0&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2
