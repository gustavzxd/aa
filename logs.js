// Carrega e exibe os logs do servidor
fetch('/logs_data', { credentials: 'same-origin' })
.then(res => res.json())
.then(data => {
    const corpo = document.getElementById('corpo');
    if (!data || data.error || data.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 4;
        td.textContent = "Nenhum log disponível.";
        tr.appendChild(td);
        corpo.appendChild(tr);
        return;
    }
    data.forEach(log => {
        const tr = document.createElement('tr');
        const tdData = document.createElement('td');
        tdData.textContent = log.data;
        tr.appendChild(tdData);
        const tdHora = document.createElement('td');
        tdHora.textContent = log.hora;
        tr.appendChild(tdHora);
        const tdUser = document.createElement('td');
        tdUser.textContent = log.usuario;
        tr.appendChild(tdUser);
        const tdAcao = document.createElement('td');
        tdAcao.textContent = log.acao;
        tr.appendChild(tdAcao);
        corpo.appendChild(tr);
    });
});