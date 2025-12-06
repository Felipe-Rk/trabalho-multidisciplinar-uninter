from fastapi import APIRouter, HTTPException, status

from app.schemas.consulta import ConsultaCreate, ConsultaRead, ConsultaUpdate
from app.core import storage

router = APIRouter()


@router.post("/", response_model=ConsultaRead, status_code=status.HTTP_201_CREATED)
def agendar_consulta(data: ConsultaCreate):
    try:
        return storage.criar_consulta(data.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[ConsultaRead])
def listar_consultas():
    return storage.listar_consultas()


@router.put("/{consulta_id}", response_model=ConsultaRead)
def atualizar_consulta(consulta_id: int, data: ConsultaUpdate):
    try:
        return storage.atualizar_consulta(
            consulta_id, data.model_dump(exclude_unset=True)
        )
    except LookupError:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
