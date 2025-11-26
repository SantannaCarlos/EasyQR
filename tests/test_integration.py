"""
Testes de integração para o fluxo completo do sistema de convites.
Testa o fluxo: criar → enviar → validar
"""
import pytest
import time
from fastapi.testclient import TestClient
from io import BytesIO

from main import app


client = TestClient(app)


class TestIntegrationFlow:
    """Testes do fluxo completo de convites."""

    def test_health_check(self):
        """Testa se a API está saudável."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_static_pages_accessible(self):
        """Testa se todas as páginas HTML estão acessíveis."""
        pages = ["/", "/login", "/dashboard", "/create", "/validate", "/list"]

        for page in pages:
            response = client.get(page)
            assert response.status_code == 200, f"Falha ao acessar {page}"
            assert "text/html" in response.headers.get("content-type", "")

    def test_complete_invite_flow(self):
        """
        Testa o fluxo completo:
        1. Criar convite e gerar QR Code
        2. Validar o QR Code gerado
        3. Verificar se o convite foi marcado como validado
        """
        # 1. Criar convite
        start_time = time.time()

        create_data = {"data": "Teste de Integração - Convite de Festa"}
        response = client.post("/api/v1/generate-qrcode", json=create_data)

        create_time = time.time() - start_time

        assert response.status_code == 200
        assert "image/png" in response.headers.get("content-type", "")

        # Verificar headers
        invite_code = response.headers.get("X-Invite-Code")
        invite_id = response.headers.get("X-Invite-ID")

        assert invite_code is not None, "Código do convite não foi retornado"
        assert invite_id is not None, "ID do convite não foi retornado"

        # Verificar se o QR Code foi gerado (tem conteúdo)
        qr_content = response.content
        assert len(qr_content) > 0, "QR Code vazio"
        assert qr_content[:8] == b'\x89PNG\r\n\x1a\n', "Não é uma imagem PNG válida"

        print(f"\n✓ Convite criado em {create_time*1000:.2f}ms")
        print(f"  Código: {invite_code}")

        # 2. Validar QR Code
        start_time = time.time()

        # Criar um arquivo de imagem mock
        files = {"file": ("qrcode.png", BytesIO(qr_content), "image/png")}
        response = client.post("/api/v1/read-qrcode", files=files)

        validate_time = time.time() - start_time

        assert response.status_code == 200
        result = response.json()

        assert result["success"] is True, "Validação falhou"
        assert result["invite_code"] == invite_code, "Código não corresponde"
        assert result["data"] == create_data["data"], "Dados não correspondem"
        assert result["is_validated"] is True, "Convite não foi marcado como validado"

        print(f"✓ Convite validado em {validate_time*1000:.2f}ms")

        # 3. Verificar se convite está na lista
        start_time = time.time()

        response = client.get("/api/v1/invites")
        list_time = time.time() - start_time

        assert response.status_code == 200
        invites = response.json()

        assert len(invites) > 0, "Nenhum convite na lista"

        # Encontrar o convite criado
        found = False
        for invite in invites:
            if invite["invite_code"] == invite_code:
                found = True
                assert invite["is_validated"] is True, "Convite não está validado na lista"
                assert invite["data"] == create_data["data"], "Dados incorretos na lista"
                break

        assert found, f"Convite {invite_code} não encontrado na lista"

        print(f"✓ Lista carregada em {list_time*1000:.2f}ms")

        # 4. Buscar convite específico
        start_time = time.time()

        response = client.get(f"/api/v1/invites/{invite_code}")
        get_time = time.time() - start_time

        assert response.status_code == 200
        invite = response.json()

        assert invite["invite_code"] == invite_code
        assert invite["is_validated"] is True
        assert invite["data"] == create_data["data"]

        print(f"✓ Convite buscado em {get_time*1000:.2f}ms")

    def test_response_time_requirements(self):
        """
        Testa se o tempo de resposta está abaixo de 1 segundo.
        Requisito: Tempo de resposta médio < 1s
        """
        operations = []

        # Teste 1: Criar convite
        for i in range(5):
            start_time = time.time()
            response = client.post(
                "/api/v1/generate-qrcode",
                json={"data": f"Teste de Performance {i}"}
            )
            elapsed = time.time() - start_time
            operations.append(("create", elapsed))
            assert response.status_code == 200

        # Teste 2: Listar convites
        for i in range(5):
            start_time = time.time()
            response = client.get("/api/v1/invites")
            elapsed = time.time() - start_time
            operations.append(("list", elapsed))
            assert response.status_code == 200

        # Calcular média
        create_times = [op[1] for op in operations if op[0] == "create"]
        list_times = [op[1] for op in operations if op[0] == "list"]

        avg_create = sum(create_times) / len(create_times)
        avg_list = sum(list_times) / len(list_times)

        print(f"\n📊 Estatísticas de Performance:")
        print(f"  Criar convite - Média: {avg_create*1000:.2f}ms")
        print(f"  Listar convites - Média: {avg_list*1000:.2f}ms")

        # Verificar requisito: < 1s
        assert avg_create < 1.0, f"Tempo de criação muito alto: {avg_create*1000:.2f}ms"
        assert avg_list < 1.0, f"Tempo de listagem muito alto: {avg_list*1000:.2f}ms"

    def test_invalid_qrcode(self):
        """Testa comportamento com QR Code inválido."""
        # Criar uma imagem PNG vazia (não é um QR Code válido)
        fake_image = BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)

        files = {"file": ("fake.png", fake_image, "image/png")}
        response = client.post("/api/v1/read-qrcode", files=files)

        assert response.status_code == 200
        result = response.json()

        # Deve retornar sucesso=false pois não conseguiu ler QR Code
        assert result["success"] is False
        assert "encontrado" in result["message"].lower()

    def test_nonexistent_invite(self):
        """Testa busca de convite que não existe."""
        response = client.get("/api/v1/invites/CODIGO_INEXISTENTE")

        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()

    def test_data_synchronization(self):
        """
        Testa sincronização de dados entre diferentes endpoints.
        Requisito: Dados sincronizados entre telas
        """
        # Criar convite
        create_data = {"data": "Teste de Sincronização"}
        response = client.post("/api/v1/generate-qrcode", json=create_data)

        invite_code = response.headers.get("X-Invite-Code")

        # Buscar em diferentes endpoints
        # 1. GET /invites/{code}
        response1 = client.get(f"/api/v1/invites/{invite_code}")
        invite1 = response1.json()

        # 2. GET /invites (lista)
        response2 = client.get("/api/v1/invites")
        invites = response2.json()
        invite2 = next((inv for inv in invites if inv["invite_code"] == invite_code), None)

        # Verificar que os dados são idênticos
        assert invite1 is not None
        assert invite2 is not None

        assert invite1["invite_code"] == invite2["invite_code"]
        assert invite1["data"] == invite2["data"]
        assert invite1["is_validated"] == invite2["is_validated"]
        assert invite1["created_at"] == invite2["created_at"]

        print("\n✓ Dados sincronizados corretamente entre endpoints")


class TestUserInterface:
    """Testes da interface do usuário."""

    def test_css_file_accessible(self):
        """Testa se o arquivo CSS está acessível."""
        response = client.get("/static/css/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_js_files_accessible(self):
        """Testa se os arquivos JavaScript estão acessíveis."""
        js_files = ["auth.js", "dashboard.js", "create.js", "validate.js", "list.js"]

        for js_file in js_files:
            response = client.get(f"/static/js/{js_file}")
            assert response.status_code == 200, f"Arquivo {js_file} não encontrado"
            assert "javascript" in response.headers.get("content-type", "").lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
