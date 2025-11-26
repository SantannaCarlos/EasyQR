document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('createInviteForm');
    form.addEventListener('submit', handleCreateInvite);
});

async function handleCreateInvite(e) {
    e.preventDefault();

    const inviteData = document.getElementById('inviteData').value;
    const createBtn = document.getElementById('createBtn');
    const errorDiv = document.getElementById('createError');
    const successDiv = document.getElementById('createSuccess');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const qrResult = document.getElementById('qrCodeResult');

    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';
    qrResult.style.display = 'none';

    createBtn.disabled = true;
    loadingSpinner.style.display = 'block';

    try {
        const startTime = performance.now();

        const { response, responseTime } = await apiRequest('/generate-qrcode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ data: inviteData })
        });

        if (response.ok) {
            const inviteCode = response.headers.get('X-Invite-Code');
            const inviteId = response.headers.get('X-Invite-ID');

            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);

            window.currentQRCode = {
                blob: blob,
                code: inviteCode,
                data: inviteData,
                imageUrl: imageUrl
            };

            document.getElementById('qrCodeImage').src = imageUrl;
            document.getElementById('inviteCode').textContent = inviteCode;
            document.getElementById('inviteInfo').textContent = inviteData;
            document.getElementById('createDate').textContent = formatDate(new Date().toISOString());

            qrResult.style.display = 'block';
            document.getElementById('createInviteForm').style.display = 'none';

            console.log(`QR Code gerado em ${responseTime.toFixed(2)}ms`);

            if (responseTime > 1000) {
                console.warn('Tempo de resposta acima do esperado (>1s)');
            }
        } else {
            const error = await response.json();
            errorDiv.textContent = error.detail || 'Erro ao gerar QR Code';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Erro:', error);
        errorDiv.textContent = 'Erro ao conectar com o servidor. Verifique se a API está rodando.';
        errorDiv.style.display = 'block';
    } finally {
        createBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
}

function downloadQRCode() {
    if (window.currentQRCode) {
        const link = document.createElement('a');
        link.href = window.currentQRCode.imageUrl;
        link.download = `qrcode_${window.currentQRCode.code}.png`;
        link.click();
    }
}

function shareQRCode() {
    if (window.currentQRCode && navigator.share) {
        const file = new File(
            [window.currentQRCode.blob],
            `qrcode_${window.currentQRCode.code}.png`,
            { type: 'image/png' }
        );

        navigator.share({
            title: 'Convite QR Code',
            text: `Código do convite: ${window.currentQRCode.code}`,
            files: [file]
        }).catch(err => {
            console.log('Erro ao compartilhar:', err);
            alert('Compartilhamento não disponível. Use o botão "Baixar" para salvar o QR Code.');
        });
    } else {
        if (window.currentQRCode) {
            navigator.clipboard.writeText(window.currentQRCode.code).then(() => {
                alert('Código do convite copiado para a área de transferência!');
            });
        }
    }
}

function resetForm() {
    document.getElementById('createInviteForm').style.display = 'block';
    document.getElementById('qrCodeResult').style.display = 'none';
    document.getElementById('inviteData').value = '';

    if (window.currentQRCode) {
        URL.revokeObjectURL(window.currentQRCode.imageUrl);
        window.currentQRCode = null;
    }
}
