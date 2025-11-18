# QR Code API

API FastAPI para geração e leitura de QR Codes com sistema de validação de convites únicos.

## 📋 Funcionalidades

- ✅ **Geração de QR Code**: Cria QR Codes únicos a partir de strings
- ✅ **Leitura de QR Code**: Decodifica QR Codes de imagens
- ✅ **Validação de Convites**: Sistema de convites únicos com validação
- ✅ **Armazenamento**: Banco de dados SQLite para persistência
- ✅ **Testes**: Suite completa de testes unitários
- ✅ **Documentação**: API documentada com Swagger/OpenAPI

## 🚀 Requisitos

- Python 3.8+
- pip

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SantannaCarlos/gpcsw.git
cd gpcsw
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Para sistemas Linux/Mac, instale dependências do pyzbar

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# macOS
brew install zbar
```

## 🏃 Como Executar

### Iniciar o servidor

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints

### 1. Gerar QR Code

**POST** `/api/v1/generate-qrcode`

Gera um QR Code único a partir de uma string e armazena no banco de dados.

**Request Body:**
```json
{
  "data": "Informações do convite"
}
```

**Response:**
- Imagem PNG do QR Code
- Headers:
  - `X-Invite-Code`: Código único do convite
  - `X-Invite-ID`: ID do convite no banco de dados

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate-qrcode" \
  -H "Content-Type: application/json" \
  -d '{"data": "Meu convite especial"}' \
  --output qrcode.png
```

**Exemplo com Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate-qrcode",
    json={"data": "Meu convite especial"}
)

# Salvar imagem
with open("qrcode.png", "wb") as f:
    f.write(response.content)

# Obter código do convite
invite_code = response.headers["X-Invite-Code"]
print(f"Código do convite: {invite_code}")
```

### 2. Ler QR Code

**POST** `/api/v1/read-qrcode`

Lê um QR Code de uma imagem e valida no banco de dados.

**Request:**
- Form-data com arquivo de imagem (campo: `file`)

**Response:**
```json
{
  "success": true,
  "invite_code": "uuid-do-convite",
  "data": "Informações do convite",
  "is_validated": true,
  "message": "QR Code lido e validado com sucesso"
}
```

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/read-qrcode" \
  -F "file=@qrcode.png"
```

**Exemplo com Python:**
```python
import requests

with open("qrcode.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/read-qrcode",
        files={"file": f}
    )

data = response.json()
print(f"Sucesso: {data['success']}")
print(f"Dados: {data['data']}")
print(f"Validado: {data['is_validated']}")
```

### 3. Consultar Convite

**GET** `/api/v1/invites/{invite_code}`

Consulta informações de um convite específico.

**Response:**
```json
{
  "id": 1,
  "invite_code": "uuid-do-convite",
  "data": "Informações do convite",
  "created_at": "2024-01-01T00:00:00",
  "is_validated": false
}
```

### 4. Listar Convites

**GET** `/api/v1/invites?skip=0&limit=100`

Lista todos os convites com paginação.

**Query Parameters:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=app tests/

# Executar testes específicos
pytest tests/test_api.py
pytest tests/test_qrcode_service.py
```

## 📁 Estrutura do Projeto

```
GPCSW/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # Endpoints da API
│   │   └── qrcode_service.py  # Serviço de QR Code
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py        # Configuração do banco
│   └── models/
│       ├── __init__.py
│       ├── invite.py          # Modelo de dados
│       └── schemas.py         # Schemas Pydantic
├── tests/
│   ├── __init__.py
│   ├── test_api.py           # Testes da API
│   └── test_qrcode_service.py # Testes do serviço
├── main.py                    # Aplicação principal
├── requirements.txt           # Dependências
├── pytest.ini                # Configuração do pytest
├── .gitignore
└── README.md
```

## 🗄️ Banco de Dados

O projeto utiliza SQLite com SQLAlchemy. O banco de dados é criado automaticamente ao iniciar a aplicação.

**Tabela `invites`:**
- `id`: Identificador único (auto-incremento)
- `invite_code`: Código único do convite (UUID)
- `data`: Informações adicionais do convite
- `qr_code_path`: Caminho do QR Code (opcional)
- `created_at`: Data/hora de criação
- `is_validated`: Flag de validação
- `validated_at`: Data/hora da validação

## 📊 Requisitos Atendidos

✅ **Funcionalidade Básica**
- Geração de QR Code a partir de string
- Leitura e decodificação de QR Code de imagem

✅ **API Simples**
- Endpoints RESTful bem definidos
- Documentação automática (Swagger/OpenAPI)

✅ **Convites Únicos**
- Sistema de geração de códigos únicos (UUID)
- Armazenamento persistente em banco de dados
- Validação automática na leitura

✅ **Testes Unitários**
- Testes para serviço de QR Code
- Testes para endpoints da API
- Cobertura de casos de sucesso e erro

✅ **Qualidade**
- QR Codes únicos e legíveis
- Dados armazenados corretamente
- Código documentado e organizado
- Tratamento de erros adequado

✅ **Performance**
- Tempo de resposta < 2 segundos
- Operações otimizadas

## 🔧 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **qrcode**: Geração de QR Codes
- **pyzbar**: Leitura de QR Codes
- **Pillow**: Processamento de imagens
- **pytest**: Framework de testes
- **uvicorn**: Servidor ASGI

## 📝 Exemplos de Uso

### Fluxo Completo

```python
import requests
from io import BytesIO

# 1. Gerar QR Code
response = requests.post(
    "http://localhost:8000/api/v1/generate-qrcode",
    json={"data": "Evento XYZ - Entrada VIP"}
)

invite_code = response.headers["X-Invite-Code"]
qr_image = response.content

# Salvar QR Code
with open("convite.png", "wb") as f:
    f.write(qr_image)

print(f"QR Code gerado! Código: {invite_code}")

# 2. Ler QR Code (simulando upload)
with open("convite.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/read-qrcode",
        files={"file": f}
    )

result = response.json()
print(f"Convite validado: {result['data']}")
print(f"Status: {'Já utilizado' if result['is_validated'] else 'Primeiro uso'}")

# 3. Consultar informações do convite
response = requests.get(
    f"http://localhost:8000/api/v1/invites/{invite_code}"
)

invite_info = response.json()
print(f"Criado em: {invite_info['created_at']}")
print(f"Validado: {invite_info['is_validated']}")
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👤 Autor

Carlos Santanna - [GitHub](https://github.com/SantannaCarlos)

## 🐛 Reportar Problemas

Se encontrar algum problema, por favor abra uma [issue](https://github.com/SantannaCarlos/gpcsw/issues).
