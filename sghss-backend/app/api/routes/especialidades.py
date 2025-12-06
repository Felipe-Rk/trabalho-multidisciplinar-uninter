from fastapi import APIRouter, HTTPException, status

from app.schemas.especialidade import (
    EspecialidadeCreate,
    EspecialidadeRead,
    EspecialidadeUpdate,
)
from app.core import storage

router = APIRouter()


@router.post("/", response_model=EspecialidadeRead, status_code=status.HTTP_201_CREATED)
def criar_especialidade(data: EspecialidadeCreate):
    try:
        return storage.criar_especialidade(data.model_dump())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma especialidade com este nome.",
        )


@router.get("/", response_model=list[EspecialidadeRead])
def listar_especialidades():
    return storage.listar_especialidades()


@router.get("/{especialidade_id}", response_model=EspecialidadeRead)
def obter_especialidade(especialidade_id: int):
    especialidade = storage.obter_especialidade(especialidade_id)
    if not especialidade:
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")
    return especialidade


@router.put("/{especialidade_id}", response_model=EspecialidadeRead)
def atualizar_especialidade(especialidade_id: int, data: EspecialidadeUpdate):
    try:
        return storage.atualizar_especialidade(
            especialidade_id, data.model_dump(exclude_unset=True)
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma especialidade com este nome.",
        )


@router.delete("/{especialidade_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_especialidade(especialidade_id: int):
    if not storage.obter_especialidade(especialidade_id):
        raise HTTPException(status_code=404, detail="Especialidade não encontrada")
    storage.deletar_especialidade(especialidade_id)
    return None
