"""
Serviço para geração e leitura de QR Codes.
"""
import io
import uuid
from typing import Optional
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode


class QRCodeService:
    """Serviço para manipulação de QR Codes."""

    @staticmethod
    def generate_unique_code() -> str:
        """
        Gera um código único usando UUID4.

        Returns:
            String com código único
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_qrcode(data: str) -> io.BytesIO:
        """
        Gera uma imagem QR Code a partir de uma string.

        Args:
            data: String com os dados para codificar no QR Code

        Returns:
            BytesIO contendo a imagem PNG do QR Code
        """
        # Criar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Criar imagem
        img = qr.make_image(fill_color="black", back_color="white")

        # Salvar em BytesIO
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return img_io

    @staticmethod
    def read_qrcode(image_bytes: bytes) -> Optional[str]:
        """
        Lê um QR Code de uma imagem.

        Args:
            image_bytes: Bytes da imagem contendo o QR Code

        Returns:
            String com os dados decodificados ou None se não encontrar QR Code
        """
        try:
            # Abrir imagem
            image = Image.open(io.BytesIO(image_bytes))

            # Decodificar QR Code
            decoded_objects = decode(image)

            if decoded_objects:
                # Retornar o primeiro QR Code encontrado
                return decoded_objects[0].data.decode('utf-8')

            return None
        except Exception as e:
            print(f"Erro ao ler QR Code: {e}")
            return None
