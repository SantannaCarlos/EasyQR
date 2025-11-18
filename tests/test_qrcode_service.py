"""
Testes unitários para o serviço de QR Code.
"""
import io
import pytest
from PIL import Image
import qrcode

from app.api.qrcode_service import QRCodeService


class TestQRCodeService:
    """Testes para QRCodeService."""

    def test_generate_unique_code(self):
        """Testa geração de código único."""
        service = QRCodeService()
        code1 = service.generate_unique_code()
        code2 = service.generate_unique_code()

        # Códigos devem ser strings
        assert isinstance(code1, str)
        assert isinstance(code2, str)

        # Códigos devem ser diferentes
        assert code1 != code2

        # Códigos devem ter formato UUID
        assert len(code1) == 36
        assert code1.count('-') == 4

    def test_generate_qrcode(self):
        """Testa geração de QR Code."""
        service = QRCodeService()
        test_data = "Test QR Code Data"

        # Gerar QR Code
        qr_image = service.generate_qrcode(test_data)

        # Verificar que retorna BytesIO
        assert isinstance(qr_image, io.BytesIO)

        # Verificar que contém dados
        qr_image.seek(0)
        image_data = qr_image.read()
        assert len(image_data) > 0

        # Verificar que é uma imagem válida
        qr_image.seek(0)
        img = Image.open(qr_image)
        assert img.format == 'PNG'

    def test_read_qrcode_valid(self):
        """Testa leitura de QR Code válido."""
        service = QRCodeService()
        test_data = "Test QR Code Data"

        # Gerar QR Code
        qr_image = service.generate_qrcode(test_data)

        # Ler QR Code
        qr_image.seek(0)
        decoded_data = service.read_qrcode(qr_image.read())

        # Verificar que decodificou corretamente
        assert decoded_data == test_data

    def test_read_qrcode_invalid(self):
        """Testa leitura de imagem sem QR Code."""
        service = QRCodeService()

        # Criar imagem em branco
        img = Image.new('RGB', (100, 100), color='white')
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Tentar ler QR Code
        decoded_data = service.read_qrcode(img_io.read())

        # Deve retornar None
        assert decoded_data is None

    def test_qrcode_roundtrip(self):
        """Testa ciclo completo: gerar e ler QR Code."""
        service = QRCodeService()
        test_data = "Complete roundtrip test"

        # Gerar QR Code
        qr_image = service.generate_qrcode(test_data)
        qr_image.seek(0)

        # Ler QR Code
        decoded_data = service.read_qrcode(qr_image.read())

        # Verificar que os dados são idênticos
        assert decoded_data == test_data
