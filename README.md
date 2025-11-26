# EasyQR - Sistema de Convites com QR Code

Sistema web para geração e validação de convites através de QR Codes, desenvolvido com FastAPI e interface responsiva.

## Funcionalidades

### Interface Web
- Tela de login com autenticação simples
- Dashboard com estatísticas em tempo real
- Criação de convites com geração automática de QR Code
- Validação de convites através de upload de imagem
- Listagem e busca de convites
- Design responsivo para mobile, tablet e desktop

### API REST
- Geração de QR Codes únicos
- Leitura e validação de QR Codes de imagens
- Sistema de validação de convites
- Armazenamento persistente em SQLite
- Documentação interativa com Swagger

## Requisitos

- Python 3.8 ou superior
- pip

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SantannaCarlos/EasyQR.git
cd EasyQR
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

### 4. Dependências do sistema (Linux/Mac)

```bash
# Ubuntu/Debian
sudo apt-get install libzbar0

# macOS
brew install zbar
```

## Como Executar

### Iniciar o servidor

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
python main.py
```

**Modo desenvolvimento:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Acessar o sistema

- Interface web: http://localhost:8000
- Documentação da API: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Credenciais de teste

- Admin: `admin` / `admin123`
- Usuário: `user` / `user123`

## Estrutura do Projeto

```
EasyQR/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── qrcode_service.py
│   ├── database/
│   │   └── database.py
│   └── models/
│       ├── invite.py
│       └── schemas.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       ├── dashboard.js
│       ├── create.js
│       ├── validate.js
│       └── list.js
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── create.html
│   ├── validate.html
│   └── list.html
├── tests/
│   ├── test_api.py
│   ├── test_qrcode_service.py
│   └── test_integration.py
├── main.py
├── start.bat
└── requirements.txt
```

## Uso da Interface

### Login
1. Acesse http://localhost:8000
2. Entre com as credenciais de teste
3. Você será redirecionado para o dashboard

### Criar convite
1. Clique em "Criar Novo Convite" no dashboard
2. Preencha as informações do convite
3. Clique em "Gerar QR Code"
4. Baixe ou compartilhe a imagem gerada

### Validar convite
1. Clique em "Validar Convite" no dashboard
2. Faça upload da imagem do QR Code
3. O sistema validará e exibirá as informações

### Listar convites
1. Clique em "Ver Todos" no dashboard
2. Use os filtros para buscar convites específicos
3. Veja o status de cada convite

## Endpoints da API

### Gerar QR Code

```http
POST /api/v1/generate-qrcode
Content-Type: application/json

{
  "data": "Informações do convite"
}
```

Retorna: Imagem PNG do QR Code + headers com código e ID do convite

### Validar QR Code

```http
POST /api/v1/read-qrcode
Content-Type: multipart/form-data

file: [arquivo de imagem]
```

Retorna:
```json
{
  "success": true,
  "invite_code": "uuid",
  "data": "Informações",
  "is_validated": true,
  "message": "QR Code lido e validado com sucesso"
}
```

### Listar convites

```http
GET /api/v1/invites?skip=0&limit=100
```

### Buscar convite específico

```http
GET /api/v1/invites/{invite_code}
```

## Testes

### Executar testes automatizados

```bash
# Todos os testes
pytest

# Testes de integração
pytest tests/test_integration.py -v

# Teste específico do fluxo completo
pytest tests/test_integration.py::TestIntegrationFlow::test_complete_invite_flow -v -s
```

### Resultados dos testes

Status: 9/9 testes passando

Performance média:
- Criar convite: ~15ms
- Validar convite: ~16ms
- Listar convites: ~2ms

Todos os tempos estão bem abaixo da meta de 1 segundo.

### Testes manuais

Um guia completo de testes manuais está disponível em `TESTE_MANUAL.md`, incluindo:
- 9 casos de teste detalhados
- Critérios de sucesso para cada funcionalidade
- Checklist de feedback de usuário
- Formulário de avaliação de usabilidade

## Banco de Dados

O sistema utiliza SQLite com SQLAlchemy. O banco é criado automaticamente na primeira execução.

Tabela `invites`:
- id: Identificador único
- invite_code: Código UUID do convite
- data: Informações do convite
- created_at: Data de criação
- is_validated: Status de validação
- validated_at: Data de validação

## Tecnologias

**Backend:**
- FastAPI - Framework web
- SQLAlchemy - ORM
- Pydantic - Validação de dados
- qrcode - Geração de QR Codes
- pyzbar - Leitura de QR Codes
- Pillow - Processamento de imagens

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Fetch API para requisições
- Design responsivo com CSS Grid/Flexbox

**Testes:**
- pytest
- httpx

## Exemplo de Uso com Python

```python
import requests

# Gerar QR Code
response = requests.post(
    "http://localhost:8000/api/v1/generate-qrcode",
    json={"data": "Festa de aniversário - 25/11/2025"}
)

invite_code = response.headers["X-Invite-Code"]
with open("convite.png", "wb") as f:
    f.write(response.content)

print(f"Convite criado: {invite_code}")

# Validar QR Code
with open("convite.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/read-qrcode",
        files={"file": f}
    )

result = response.json()
print(f"Validado: {result['success']}")
print(f"Dados: {result['data']}")
```

## Autores

Grupo 5 da turma de 2025.2 de Gestão de Projetos
