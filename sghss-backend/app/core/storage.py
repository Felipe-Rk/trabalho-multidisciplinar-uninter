"""
Armazena dados em memória para uso acadêmico (sem banco real).
"""
from __future__ import annotations

from datetime import datetime

_pacientes: list[dict] = []
_especialidades: list[dict] = []
_medicos: list[dict] = []
_consultas: list[dict] = []


def _next_id(registros: list[dict]) -> int:
    return (max((item["id"] for item in registros), default=0) + 1) if registros else 1


# Pacientes
def criar_paciente(data: dict) -> dict:
    if any(p["cpf"] == data["cpf"] for p in _pacientes):
        raise ValueError("CPF duplicado")
    paciente = data | {"id": _next_id(_pacientes)}
    _pacientes.append(paciente)
    return paciente


def listar_pacientes() -> list[dict]:
    return list(_pacientes)


def obter_paciente(paciente_id: int) -> dict | None:
    return next((p for p in _pacientes if p["id"] == paciente_id), None)


def atualizar_paciente(paciente_id: int, data: dict) -> dict:
    paciente = obter_paciente(paciente_id)
    if not paciente:
        raise LookupError("Paciente não encontrado")
    paciente.update(data)
    return paciente


def deletar_paciente(paciente_id: int) -> None:
    global _pacientes
    _pacientes = [p for p in _pacientes if p["id"] != paciente_id]


# Especialidades
def criar_especialidade(data: dict) -> dict:
    if any(e["nome"].lower() == data["nome"].lower() for e in _especialidades):
        raise ValueError("Especialidade duplicada")
    especialidade = data | {"id": _next_id(_especialidades)}
    _especialidades.append(especialidade)
    return especialidade


def listar_especialidades() -> list[dict]:
    return list(_especialidades)


def obter_especialidade(especialidade_id: int) -> dict | None:
    return next((e for e in _especialidades if e["id"] == especialidade_id), None)


def atualizar_especialidade(especialidade_id: int, data: dict) -> dict:
    especialidade = obter_especialidade(especialidade_id)
    if not especialidade:
        raise LookupError("Especialidade não encontrada")
    especialidade.update(data)
    return especialidade


def deletar_especialidade(especialidade_id: int) -> None:
    global _especialidades
    _especialidades = [e for e in _especialidades if e["id"] != especialidade_id]


# Médicos
def criar_medico(data: dict) -> dict:
    if any(m["crm"] == data["crm"] for m in _medicos):
        raise ValueError("CRM duplicado")
    if not obter_especialidade(data["especialidade_id"]):
        raise LookupError("Especialidade não encontrada")
    medico = data | {"id": _next_id(_medicos)}
    _medicos.append(medico)
    return medico


def listar_medicos() -> list[dict]:
    return list(_medicos)


def obter_medico(medico_id: int) -> dict | None:
    return next((m for m in _medicos if m["id"] == medico_id), None)


def atualizar_medico(medico_id: int, data: dict) -> dict:
    medico = obter_medico(medico_id)
    if not medico:
        raise LookupError("Médico não encontrado")
    if "crm" in data and any(m["crm"] == data["crm"] and m["id"] != medico_id for m in _medicos):
        raise ValueError("CRM duplicado")
    if "especialidade_id" in data and not obter_especialidade(data["especialidade_id"]):
        raise LookupError("Especialidade não encontrada")
    medico.update(data)
    return medico


def deletar_medico(medico_id: int) -> None:
    global _medicos
    _medicos = [m for m in _medicos if m["id"] != medico_id]


# Consultas
def criar_consulta(data: dict) -> dict:
    if not obter_paciente(data["paciente_id"]):
        raise LookupError("Paciente não encontrado")
    if not obter_medico(data["medico_id"]):
        raise LookupError("Médico não encontrado")
    consulta = data | {"id": _next_id(_consultas)}
    # Normaliza datetime em string ISO
    if isinstance(consulta.get("data_hora"), datetime):
        consulta["data_hora"] = consulta["data_hora"].isoformat()
    _consultas.append(consulta)
    return consulta


def listar_consultas() -> list[dict]:
    return list(_consultas)


def obter_consulta(consulta_id: int) -> dict | None:
    return next((c for c in _consultas if c["id"] == consulta_id), None)


def atualizar_consulta(consulta_id: int, data: dict) -> dict:
    consulta = obter_consulta(consulta_id)
    if not consulta:
        raise LookupError("Consulta não encontrada")
    consulta.update(data)
    return consulta


# Utilitário de teste
def resetar_tudo() -> None:
    global _pacientes, _especialidades, _medicos, _consultas
    _pacientes = []
    _especialidades = []
    _medicos = []
    _consultas = []
