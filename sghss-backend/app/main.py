from fastapi import FastAPI

from app.api.routes import pacientes, consultas, auth, medicos, especialidades

app = FastAPI(
    title="SGHSS - VidaPlus API",
    description="API de Gestão Hospitalar e de Serviços de Saúde (dados em memória)",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(pacientes.router, prefix="/pacientes", tags=["Pacientes"])
app.include_router(consultas.router, prefix="/consultas", tags=["Consultas"])
app.include_router(medicos.router, prefix="/medicos", tags=["Medicos"])
app.include_router(especialidades.router, prefix="/especialidades", tags=["Especialidades"])
