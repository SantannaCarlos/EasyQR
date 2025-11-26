let allInvites = [];

document.addEventListener('DOMContentLoaded', async function() {
    await loadInvites();
});

async function loadInvites() {
    const invitesList = document.getElementById('invitesList');
    const emptyState = document.getElementById('emptyState');

    try {
        const { response, responseTime } = await apiRequest('/invites');

        if (response.ok) {
            allInvites = await response.json();

            console.log(`${allInvites.length} convites carregados em ${responseTime.toFixed(2)}ms`);

            if (allInvites.length === 0) {
                invitesList.style.display = 'none';
                emptyState.style.display = 'block';
            } else {
                invitesList.innerHTML = '';
                renderInvites(allInvites);
            }
        } else {
            throw new Error('Erro ao carregar convites');
        }
    } catch (error) {
        console.error('Erro:', error);
        invitesList.innerHTML = `
            <div class="error-message">
                Erro ao carregar convites. Verifique se a API está rodando.
            </div>
        `;
    }
}

function renderInvites(invites) {
    const invitesList = document.getElementById('invitesList');

    if (invites.length === 0) {
        invitesList.innerHTML = `
            <div class="empty-state">
                <p>Nenhum convite encontrado com os filtros aplicados.</p>
            </div>
        `;
        return;
    }

    invitesList.innerHTML = invites.map(invite => `
        <div class="invite-card" data-code="${invite.invite_code}" data-validated="${invite.is_validated}">
            <div class="invite-card-header">
                <code>${invite.invite_code}</code>
                <span class="badge ${invite.is_validated ? 'validated' : 'pending'}">
                    ${invite.is_validated ? 'Validado' : 'Pendente'}
                </span>
            </div>
            <div class="invite-card-body">
                <p><strong>Informações:</strong> ${invite.data || 'N/A'}</p>
                <p><strong>Criado em:</strong> ${formatDate(invite.created_at)}</p>
                ${invite.is_validated && invite.validated_at ?
                    `<p><strong>Validado em:</strong> ${formatDate(invite.validated_at)}</p>` :
                    ''}
            </div>
        </div>
    `).join('');
}

function filterInvites() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;

    let filtered = allInvites;

    if (searchTerm) {
        filtered = filtered.filter(invite =>
            invite.invite_code.toLowerCase().includes(searchTerm) ||
            (invite.data && invite.data.toLowerCase().includes(searchTerm))
        );
    }

    if (statusFilter !== 'all') {
        const isValidated = statusFilter === 'validated';
        filtered = filtered.filter(invite => invite.is_validated === isValidated);
    }

    renderInvites(filtered);
}

async function refreshList() {
    document.getElementById('searchInput').value = '';
    document.getElementById('statusFilter').value = 'all';

    const invitesList = document.getElementById('invitesList');
    invitesList.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Carregando convites...</p>
        </div>
    `;

    await loadInvites();
}
