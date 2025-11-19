"""
Rotas da API para geração e leitura de QR Codes.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.invite import Invite
from app.models.schemas import InviteCreate, InviteResponse, QRCodeReadResponse
from app.api.qrcode_service import QRCodeService

router = APIRouter()
qr_service = QRCodeService()


@router.post("/generate-qrcode", response_class=StreamingResponse)
async def generate_qrcode(
    invite_data: InviteCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint para gerar QR Code a partir de uma string.

    Args:
        invite_data: Dados do convite (string)
        db: Sessão do banco de dados

    Returns:
        Imagem PNG do QR Code

    Raises:
        HTTPException: Se houver erro ao gerar o QR Code
    """
    try:
        # Gerar código único para o convite
        invite_code = qr_service.generate_unique_code()

        # Criar convite no banco de dados
        db_invite = Invite(
            invite_code=invite_code,
            data=invite_data.data
        )
        db.add(db_invite)
        db.commit()
        db.refresh(db_invite)

        # Gerar QR Code com o código único
        qr_image = qr_service.generate_qrcode(invite_code)

        # Retornar imagem como resposta
        return StreamingResponse(
            qr_image,
            media_type="image/png",
            headers={
                "Content-Disposition": f"inline; filename=qrcode_{invite_code}.png",
                "X-Invite-Code": invite_code,
                "X-Invite-ID": str(db_invite.id)
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao gerar QR Code: {str(e)}")


@router.post("/read-qrcode", response_model=QRCodeReadResponse)
async def read_qrcode(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint para ler QR Code de uma imagem e validar no banco de dados.

    Args:
        file: Arquivo de imagem contendo o QR Code
        db: Sessão do banco de dados

    Returns:
        Informações do convite decodificado

    Raises:
        HTTPException: Se houver erro ao ler o QR Code
    """
    try:
        # Validar tipo de arquivo
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Arquivo deve ser uma imagem"
            )

        # Ler bytes da imagem
        image_bytes = await file.read()

        # Decodificar QR Code
        invite_code = qr_service.read_qrcode(image_bytes)

        if not invite_code:
            return QRCodeReadResponse(
                success=False,
                message="Nenhum QR Code encontrado na imagem"
            )

        # Buscar convite no banco de dados
        db_invite = db.query(Invite).filter(
            Invite.invite_code == invite_code
        ).first()

        if not db_invite:
            return QRCodeReadResponse(
                success=False,
                invite_code=invite_code,
                message="Convite não encontrado no banco de dados"
            )

        # Marcar como validado se ainda não foi
        if not db_invite.is_validated:
            db_invite.is_validated = True
            db_invite.validated_at = datetime.utcnow()
            db.commit()

        return QRCodeReadResponse(
            success=True,
            invite_code=invite_code,
            data=db_invite.data,
            is_validated=db_invite.is_validated,
            message="QR Code lido e validado com sucesso"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler QR Code: {str(e)}")


@router.get("/invites/{invite_code}", response_model=InviteResponse)
async def get_invite(invite_code: str, db: Session = Depends(get_db)):
    """
    Endpoint para consultar informações de um convite pelo código.

    Args:
        invite_code: Código único do convite
        db: Sessão do banco de dados

    Returns:
        Informações do convite

    Raises:
        HTTPException: Se o convite não for encontrado
    """
    db_invite = db.query(Invite).filter(
        Invite.invite_code == invite_code.strip()
    ).first()

    if not db_invite:
        raise HTTPException(status_code=404, detail="Convite não encontrado")

    return db_invite


@router.get("/invites", response_model=list[InviteResponse])
async def list_invites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Endpoint para listar todos os convites.

    Args:
        skip: Número de registros para pular (paginação)
        limit: Número máximo de registros para retornar
        db: Sessão do banco de dados

    Returns:
        Lista de convites
    """
    invites = db.query(Invite).offset(skip).limit(limit).all()
    return invites
