from pydantic import BaseModel, ConfigDict


class MedicoBase(BaseModel):
    nome: str
    crm: str
    especialidade_id: int


class MedicoCreate(MedicoBase):
    pass


class MedicoUpdate(BaseModel):
    nome: str | None = None
    crm: str | None = None
    especialidade_id: int | None = None


class MedicoRead(MedicoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
