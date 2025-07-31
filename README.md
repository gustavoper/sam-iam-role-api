
# 🚀 AWS Lambda IAM Role Manager

Este projeto implementa uma API REST serverless na AWS que permite **criar** e **consultar** roles do IAM via dois endpoints expostos no API Gateway. A API é construída com AWS Lambda (Python), testada com `pytest` e empacotada para execução serverless.

---

## 📌 Funcionalidades

- ✅ **POST /roles**  
  Cria uma nova role IAM com política de confiança para execução por funções Lambda.

- ✅ **GET /roles/{name}**  
  Retorna os detalhes da role IAM, incluindo ARN e data de criação.

---

## 📁 Estrutura do Projeto

```bash
.
├── lambda/
│   ├── create_role.py       # Lambda para criação de roles
│   └── get_role.py          # Lambda para consulta de roles
├── tests/
│   ├── test_create_role.py  # Testes para criação
│   └── test_get_role.py     # Testes para consulta
├── template.yaml            # SAM Template
├── requirements.txt         # Dependências
└── README.md                # Este arquivo
```

---

## ▶️ Deploy 

Recomendo fortemente o uso do `sam`

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html





## 🧪 Testes Locais

### 1. Instalar dependências:

```bash
pip install -r requirements.txt
```

### 2. Executar testes:

```bash
pytest tests/
```

---

## 🔄 Exemplo de uso

### ✅ Criar Role

```http
POST /roles
Content-Type: application/json

{
  "role_name": "MinhaNovaRole"
}
```

**Resposta:**
```json
{
  "message": "Role criada com sucesso",
  "arn": "arn:aws:iam::123456789012:role/MinhaNovaRole"
}
```

---

### 🔍 Consultar Role

```http
GET /roles/MinhaNovaRole
```

**Resposta:**
```json
{
  "role_name": "MinhaNovaRole",
  "arn": "arn:aws:iam::123456789012:role/MinhaNovaRole",
  "created": "2025-07-31T03:13:57+00:00"
}
```

---

## 🛡️ WIP


- Limitar as ações com Scope Policies
- Authenticação (Cognito, JWT, APIkey, ...)
- Observability 

---

## 📄 Licença

MIT © 2025 Gustavo Pereira



###

Comandos para não esquecer:


```
sam deploy --guided

sam sync --watch


sam delete
```