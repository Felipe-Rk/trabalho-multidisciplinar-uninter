from fastapi import APIRouter, HTTPException, status

from app.schemas.medico import MedicoCreate, MedicoRead, MedicoUpdate
from app.core import storage

router = APIRouter()


@router.post("/", response_model=MedicoRead, status_code=status.HTTP_201_CREATED)
def criar_medico(data: MedicoCreate):
    try:
        return storage.criar_medico(data.model_dump())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um médico com este CRM.",
        )
    except LookupError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[MedicoRead])
def listar_medicos():
    return storage.listar_medicos()


@router.get("/{medico_id}", response_model=MedicoRead)
def obter_medico(medico_id: int):
    medico = storage.obter_medico(medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    return medico


@router.put("/{medico_id}", response_model=MedicoRead)
def atualizar_medico(medico_id: int, data: MedicoUpdate):
    try:
        return storage.atualizar_medico(
            medico_id, data.model_dump(exclude_unset=True)
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um médico com este CRM.",
        )


@router.delete("/{medico_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_medico(medico_id: int):
    if not storage.obter_medico(medico_id):
        raise HTTPException(status_code=404, detail="Médico não encontrado")
    storage.deletar_medico(medico_id)
    return None
