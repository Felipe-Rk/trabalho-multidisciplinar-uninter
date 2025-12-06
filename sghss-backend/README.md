# SGHSS – Back-end (mock em memória)

API simples em FastAPI para o projeto multidisciplinar VidaPlus. Os dados são mantidos em memória (mock), sem banco de dados real, apenas para fins acadêmicos.

## Tecnologias
- Python 3.12+
- FastAPI + Uvicorn
- Pydantic v2
- Pytest (testes básicos)

## Instalação
```bash
pip install -r requirements.txt
```

## Rodar a API
```bash
uvicorn app.main:app --reload
```
Docs automáticas: acesse `http://localhost:8000/docs`.

## Testes
```bash
pytest -q
```

## Endpoints principais
- `POST /auth/login` – login fake (email: `admin@vidaplus.com`, senha: `admin`)
- `POST /especialidades/`, `GET /especialidades/`
- `POST /medicos/`, `GET /medicos/`
- `POST /pacientes/`, `GET /pacientes/`, `PUT /pacientes/{id}`, `DELETE /pacientes/{id}`
- `POST /consultas/`, `GET /consultas/`, `PUT /consultas/{id}`

## Fluxo sugerido
1. Criar especialidade.
2. Criar médico referenciando a especialidade.
3. Criar paciente.
4. Agendar consulta ligando paciente e médico.
