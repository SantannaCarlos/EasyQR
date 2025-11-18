"""
Schemas Pydantic para validação de dados da API.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class InviteCreate(BaseModel):
    """Schema para criação de convite."""
    data: str = Field(..., description="String com informações do convite")


class InviteResponse(BaseModel):
    """Schema para resposta de convite criado."""
    id: int
    invite_code: str
    data: Optional[str] = None
    created_at: datetime
    is_validated: bool

    class Config:
        from_attributes = True


class QRCodeReadResponse(BaseModel):
    """Schema para resposta de leitura de QR Code."""
    success: bool
    invite_code: Optional[str] = None
    data: Optional[str] = None
    is_validated: bool = False
    message: str
