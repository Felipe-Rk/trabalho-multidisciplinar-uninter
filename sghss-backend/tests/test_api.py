from datetime import date, datetime
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.main import app  # noqa: E402
from app.core import storage  # noqa: E402

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    storage.resetar_tudo()
    yield
    storage.resetar_tudo()


def test_login_ok():
    resp = client.post(
        "/auth/login",
        json={"email": "admin@vidaplus.com", "senha": "admin"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"] == "fake-token-123"
    assert body["token_type"] == "bearer"


def test_login_fail():
    resp = client.post(
        "/auth/login",
        json={"email": "admin@vidaplus.com", "senha": "errada"},
    )
    assert resp.status_code == 401


def test_paciente_crud():
    paciente_data = {
        "nome": "Joao Teste",
        "cpf": "12345678900",
        "data_nascimento": str(date(1990, 1, 1)),
        "telefone": "11999999999",
        "email": "joao@example.com",
    }
    resp = client.post("/pacientes/", json=paciente_data)
    assert resp.status_code == 201
    created = resp.json()
    paciente_id = created["id"]

    resp = client.get(f"/pacientes/{paciente_id}")
    assert resp.status_code == 200
    assert resp.json()["cpf"] == paciente_data["cpf"]

    resp = client.put(
        f"/pacientes/{paciente_id}",
        json={"telefone": "11888888888"},
    )
    assert resp.status_code == 200
    assert resp.json()["telefone"] == "11888888888"

    resp = client.delete(f"/pacientes/{paciente_id}")
    assert resp.status_code == 204
    resp = client.get(f"/pacientes/{paciente_id}")
    assert resp.status_code == 404


def test_fluxo_consulta():
    resp = client.post("/especialidades/", json={"nome": "Cardiologia"})
    assert resp.status_code == 201
    especialidade_id = resp.json()["id"]

    resp = client.post(
        "/medicos/",
        json={"nome": "Dr. House", "crm": "CRM123", "especialidade_id": especialidade_id},
    )
    assert resp.status_code == 201
    medico_id = resp.json()["id"]

    resp = client.post(
        "/pacientes/",
        json={
            "nome": "Paciente Consulta",
            "cpf": "98765432100",
            "data_nascimento": str(date(1985, 5, 5)),
            "telefone": "11777777777",
            "email": "paciente@example.com",
        },
    )
    assert resp.status_code == 201
    paciente_id = resp.json()["id"]

    resp = client.post(
        "/consultas/",
        json={
            "paciente_id": paciente_id,
            "medico_id": medico_id,
            "data_hora": datetime(2030, 1, 1, 10, 0).isoformat(),
            "status": "AGENDADA",
            "observacoes": "Teste",
        },
    )
    assert resp.status_code == 201
    consulta_id = resp.json()["id"]

    resp = client.put(
        f"/consultas/{consulta_id}",
        json={"status": "CANCELADA", "observacoes": "Cancelada pelo paciente"},
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["status"] == "CANCELADA"
    assert updated["observacoes"] == "Cancelada pelo paciente"
