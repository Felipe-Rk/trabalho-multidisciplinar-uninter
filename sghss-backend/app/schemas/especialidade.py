from pydantic import BaseModel, ConfigDict


class EspecialidadeBase(BaseModel):
    nome: str


class EspecialidadeCreate(EspecialidadeBase):
    pass


class EspecialidadeUpdate(BaseModel):
    nome: str | None = None


class EspecialidadeRead(EspecialidadeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
