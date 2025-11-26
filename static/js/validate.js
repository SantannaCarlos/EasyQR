document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('validateForm');
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('qrCodeFile');

    uploadArea.addEventListener('click', () => fileInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Seleção de arquivo
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    form.addEventListener('submit', handleValidate);
});

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        alert('Por favor, selecione uma imagem válida.');
        return;
    }

    window.selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('imagePreview').style.display = 'block';
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('validateBtn').disabled = false;
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    window.selectedFile = null;
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('validateBtn').disabled = true;
    document.getElementById('qrCodeFile').value = '';
}

async function handleValidate(e) {
    e.preventDefault();

    if (!window.selectedFile) {
        alert('Por favor, selecione uma imagem do QR Code.');
        return;
    }

    const validateBtn = document.getElementById('validateBtn');
    const errorDiv = document.getElementById('validateError');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const validationResult = document.getElementById('validationResult');

    errorDiv.style.display = 'none';
    validationResult.style.display = 'none';

    validateBtn.disabled = true;
    loadingSpinner.style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('file', window.selectedFile);

        const startTime = performance.now();

        const { response, responseTime } = await apiRequest('/read-qrcode', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        validationResult.style.display = 'block';

        if (result.success && result.invite_code) {
            document.getElementById('successResult').style.display = 'block';
            document.getElementById('errorResult').style.display = 'none';

            document.getElementById('resultCode').textContent = result.invite_code;
            document.getElementById('resultData').textContent = result.data || 'N/A';

            const statusBadge = document.getElementById('resultStatus');
            if (result.is_validated) {
                statusBadge.textContent = 'Validado';
                statusBadge.className = 'badge validated';
            } else {
                statusBadge.textContent = 'Pendente';
                statusBadge.className = 'badge pending';
            }

            document.getElementById('validationTime').textContent = formatDate(new Date().toISOString());

            console.log(`Validação concluída em ${responseTime.toFixed(2)}ms`);

            if (responseTime > 1000) {
                console.warn('Tempo de resposta acima do esperado (>1s)');
            }
        } else {
            document.getElementById('successResult').style.display = 'none';
            document.getElementById('errorResult').style.display = 'block';
            document.getElementById('errorMessage').textContent = result.message || 'QR Code inválido ou não encontrado.';
        }

        document.getElementById('validateForm').style.display = 'none';

    } catch (error) {
        console.error('Erro:', error);
        errorDiv.textContent = 'Erro ao conectar com o servidor. Verifique se a API está rodando.';
        errorDiv.style.display = 'block';
    } finally {
        validateBtn.disabled = false;
        loadingSpinner.style.display = 'none';
    }
}

function resetValidation() {
    document.getElementById('validateForm').style.display = 'block';
    document.getElementById('validationResult').style.display = 'none';
    clearImage();
}
