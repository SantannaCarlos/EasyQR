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
    try:
        invite_code = qr_service.generate_unique_code()

        db_invite = Invite(
            invite_code=invite_code,
            data=invite_data.data
        )
        db.add(db_invite)
        db.commit()
        db.refresh(db_invite)

        qr_image = qr_service.generate_qrcode(invite_code)
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
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")

        image_bytes = await file.read()
        invite_code = qr_service.read_qrcode(image_bytes)

        if not invite_code:
            return QRCodeReadResponse(
                success=False,
                message="Nenhum QR Code encontrado na imagem"
            )

        db_invite = db.query(Invite).filter(Invite.invite_code == invite_code).first()

        if not db_invite:
            return QRCodeReadResponse(
                success=False,
                invite_code=invite_code,
                message="Convite não encontrado no banco de dados"
            )

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
    db_invite = db.query(Invite).filter(Invite.invite_code == invite_code.strip()).first()

    if not db_invite:
        raise HTTPException(status_code=404, detail="Convite não encontrado")

    return db_invite


@router.get("/invites", response_model=list[InviteResponse])
async def list_invites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Invite).offset(skip).limit(limit).all()
