from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """Configuração simples para fins acadêmicos (sem BD real)."""

    model_config = ConfigDict(extra="ignore")
    SECRET_KEY: str = "changeme"


settings = Settings()
