// Inicializa o mapa centrado no Brasil
const map = L.map('map').setView([-14.235, -51.925], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let marker = null;

// Ao clicar no mapa, atualiza latitude/longitude e mostra marcador
map.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(6);
    const lon = e.latlng.lng.toFixed(6);
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lon;
    document.getElementById('endereco').value = `(${lat}, ${lon})`;
    if (marker) {
        marker.setLatLng(e.latlng);
    } else {
        marker = L.marker(e.latlng).addTo(map);
    }
});

// Busca de endereço simples usando Nominatim
document.getElementById('searchBtn').onclick = function() {
    const addr = document.getElementById('address').value;
    if (!addr) return;
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(addr)}`)
    .then(res => res.json())
    .then(results => {
        if (results && results[0]) {
            const lat = parseFloat(results[0].lat);
            const lon = parseFloat(results[0].lon);
            map.setView([lat, lon], 16);
            map.fireEvent('click', { latlng: L.latLng(lat, lon) });
        } else {
            alert('Endereço não encontrado.');
        }
    });
};

// Salva a ocorrência via API
document.getElementById('salvarBtn').onclick = function() {
    const tipo = document.getElementById('tipo').value;
    const prioridade = document.getElementById('prioridade').value;
    const endereco = document.getElementById('endereco').value;
    const lat = document.getElementById('latitude').value;
    const lon = document.getElementById('longitude').value;
    if (!tipo || !prioridade || !endereco || !lat || !lon) {
        alert('Preencha todos os campos.');
        return;
    }
    fetch('/registrar_ocorrencia', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tipo: tipo,
            prioridade: prioridade,
            descricao: '',   // campo descrição removido neste layout
            endereco: endereco,
            lat: parseFloat(lat),
            lon: parseFloat(lon)
        })
    })
    .then(res => {
        if (res.ok) {
            alert('Ocorrência registrada com sucesso.');
        } else {
            alert('Falha ao registrar ocorrência.');
        }
    });
};
    