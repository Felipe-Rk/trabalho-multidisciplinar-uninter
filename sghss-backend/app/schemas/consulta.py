from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    data_hora: datetime
    status: str | None = "AGENDADA"
    observacoes: str | None = None


class ConsultaCreate(ConsultaBase):
    pass


class ConsultaUpdate(BaseModel):
    status: str | None = None
    observacoes: str | None = None


class ConsultaRead(ConsultaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
