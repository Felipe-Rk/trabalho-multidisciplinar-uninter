from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict


class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date
    telefone: str | None = None
    email: EmailStr | None = None


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
    nome: str | None = None
    telefone: str | None = None
    email: EmailStr | None = None


class PacienteRead(PacienteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
