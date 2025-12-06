from fastapi import APIRouter, HTTPException, status

from app.schemas.paciente import PacienteCreate, PacienteRead, PacienteUpdate
from app.core import storage

router = APIRouter()


@router.post("/", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def criar_paciente(data: PacienteCreate):
    try:
        return storage.criar_paciente(data.model_dump())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um paciente cadastrado com este CPF.",
        )


@router.get("/", response_model=list[PacienteRead])
def listar_pacientes():
    return storage.listar_pacientes()


@router.get("/{paciente_id}", response_model=PacienteRead)
def obter_paciente(paciente_id: int):
    paciente = storage.obter_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


@router.put("/{paciente_id}", response_model=PacienteRead)
def atualizar_paciente(paciente_id: int, data: PacienteUpdate):
    try:
        return storage.atualizar_paciente(
            paciente_id, data.model_dump(exclude_unset=True)
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(paciente_id: int):
    paciente = storage.obter_paciente(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    storage.deletar_paciente(paciente_id)
    return None
