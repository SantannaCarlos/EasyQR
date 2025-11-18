"""
Modelo de dados para convites com QR Code.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database.database import Base


class Invite(Base):
    """
    Modelo para armazenar convites únicos com QR Code.

    Attributes:
        id: Identificador único do convite
        invite_code: Código único do convite (usado para gerar QR Code)
        data: Informações adicionais do convite (JSON string)
        qr_code_path: Caminho onde o QR Code foi salvo (opcional)
        created_at: Data e hora de criação
        is_validated: Indica se o convite já foi validado/usado
        validated_at: Data e hora da validação
    """
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    invite_code = Column(String, unique=True, index=True, nullable=False)
    data = Column(String, nullable=True)
    qr_code_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_validated = Column(Boolean, default=False)
    validated_at = Column(DateTime, nullable=True)
