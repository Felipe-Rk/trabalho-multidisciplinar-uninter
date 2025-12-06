from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    # Aqui você poderia consultar o banco (Usuario), mas para o trabalho
    # podemos simular um login bem simples.
    if data.email != "admin@vidaplus.com" or data.senha != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    # Token "fake" apenas para fins acadêmicos
    return TokenResponse(access_token="fake-token-123")
