document.addEventListener('DOMContentLoaded', async function() {
    await loadStats();
});

async function loadStats() {
    try {
        const { response, responseTime } = await apiRequest('/invites');

        if (response.ok) {
            const invites = await response.json();
            const total = invites.length;
            const validated = invites.filter(inv => inv.is_validated).length;
            const pending = total - validated;

            document.getElementById('totalInvites').textContent = total;
            document.getElementById('validatedInvites').textContent = validated;
            document.getElementById('pendingInvites').textContent = pending;

            if (responseTime > 1000) {
                console.warn(`Slow API response: ${responseTime.toFixed(2)}ms`);
            }
        } else {
            console.error('Erro ao carregar estatísticas');
            document.getElementById('totalInvites').textContent = '0';
            document.getElementById('validatedInvites').textContent = '0';
            document.getElementById('pendingInvites').textContent = '0';
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
        document.getElementById('totalInvites').textContent = 'Erro';
        document.getElementById('validatedInvites').textContent = 'Erro';
        document.getElementById('pendingInvites').textContent = 'Erro';
    }
}
