document.addEventListener('DOMContentLoaded', function () {
    fetchMarketData();
    setInterval(fetchMarketData, 60000);
});

async function fetchMarketData() {
    try {
        const response = await fetch('/api/acciones_data/');
        
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();

        renderTable(data.America || [], '#america-data');
        renderTable(data.Europe || [], '#europe-data');

    } catch (error) {
        console.error('Error al cargar los datos del mercado:', error);
        document.getElementById('america-data').innerHTML = 
            '<tr><td colspan="3" class="text-center text-danger">Sin conexión</td></tr>';
        document.getElementById('europe-data').innerHTML = 
            '<tr><td colspan="3" class="text-center text-danger">Sin conexión</td></tr>';
    }
}

function renderTable(items, selector) {
    const tbody = document.querySelector(selector);
    if (!tbody) return;

    if (items.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">Sin datos</td></tr>';
        return;
    }

    tbody.innerHTML = '';
    items.forEach(item => {
        const isUp = item.change_abs >= 0;
        const changeClass = isUp ? 'up' : 'down';
        const sign = isUp ? '+' : '';

        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="${changeClass}">${item.symbol}</td>
            <td>${item.last}</td>
            <td>
                ${sign}${item.change_abs}<br>
                <small>${sign}${item.change_pct}%</small>
            </td>
        `;
        tbody.appendChild(row);
    });
}
