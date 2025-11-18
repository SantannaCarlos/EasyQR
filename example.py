"""
Exemplo de uso da API QR Code.

Este script demonstra como usar a API para:
1. Gerar QR Codes
2. Ler QR Codes
3. Consultar convites

Certifique-se de que a API está rodando antes de executar este exemplo.
Execute: python main.py
"""
import requests
import time


def example_generate_qrcode():
    """Exemplo: Gerar QR Code."""
    print("\n=== Exemplo 1: Gerar QR Code ===")

    url = "http://localhost:8000/api/v1/generate-qrcode"
    data = {
        "data": "Evento Python Brasil 2024 - Entrada VIP"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # Salvar QR Code
        filename = "convite_exemplo.png"
        with open(filename, "wb") as f:
            f.write(response.content)

        invite_code = response.headers.get("X-Invite-Code")
        invite_id = response.headers.get("X-Invite-ID")

        print(f"✅ QR Code gerado com sucesso!")
        print(f"   Arquivo: {filename}")
        print(f"   Código do convite: {invite_code}")
        print(f"   ID: {invite_id}")

        return filename, invite_code
    else:
        print(f"❌ Erro: {response.status_code}")
        return None, None


def example_read_qrcode(filename):
    """Exemplo: Ler QR Code."""
    print("\n=== Exemplo 2: Ler QR Code ===")

    url = "http://localhost:8000/api/v1/read-qrcode"

    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "image/png")}
            response = requests.post(url, files=files)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ QR Code lido com sucesso!")
            print(f"   Sucesso: {data['success']}")
            print(f"   Código: {data['invite_code']}")
            print(f"   Dados: {data['data']}")
            print(f"   Validado: {data['is_validated']}")
            print(f"   Mensagem: {data['message']}")
            return data['invite_code']
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   {response.json()}")
            return None
    except FileNotFoundError:
        print(f"❌ Arquivo {filename} não encontrado")
        return None


def example_get_invite(invite_code):
    """Exemplo: Consultar convite."""
    print("\n=== Exemplo 3: Consultar Convite ===")

    url = f"http://localhost:8000/api/v1/invites/{invite_code}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Convite encontrado!")
        print(f"   ID: {data['id']}")
        print(f"   Código: {data['invite_code']}")
        print(f"   Dados: {data['data']}")
        print(f"   Criado em: {data['created_at']}")
        print(f"   Validado: {data['is_validated']}")
    else:
        print(f"❌ Erro: {response.status_code}")
        print(f"   {response.json()}")


def example_list_invites():
    """Exemplo: Listar convites."""
    print("\n=== Exemplo 4: Listar Convites ===")

    url = "http://localhost:8000/api/v1/invites?skip=0&limit=5"

    response = requests.get(url)

    if response.status_code == 200:
        invites = response.json()
        print(f"✅ {len(invites)} convite(s) encontrado(s):")
        for invite in invites:
            print(f"\n   ID: {invite['id']}")
            print(f"   Código: {invite['invite_code'][:20]}...")
            print(f"   Dados: {invite['data']}")
            print(f"   Validado: {invite['is_validated']}")
    else:
        print(f"❌ Erro: {response.status_code}")


def check_api_health():
    """Verifica se a API está rodando."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def main():
    """Executa todos os exemplos."""
    print("=" * 50)
    print("API QR Code - Exemplos de Uso")
    print("=" * 50)

    # Verificar se a API está rodando
    if not check_api_health():
        print("\n❌ A API não está rodando!")
        print("   Execute: python main.py")
        return

    print("\n✅ API está rodando\n")

    # Exemplo 1: Gerar QR Code
    filename, invite_code = example_generate_qrcode()

    if filename and invite_code:
        # Aguardar um pouco
        time.sleep(0.5)

        # Exemplo 2: Ler QR Code
        read_code = example_read_qrcode(filename)

        if read_code:
            # Aguardar um pouco
            time.sleep(0.5)

            # Exemplo 3: Consultar convite
            example_get_invite(read_code)

    # Exemplo 4: Listar convites
    time.sleep(0.5)
    example_list_invites()

    print("\n" + "=" * 50)
    print("Exemplos concluídos!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
