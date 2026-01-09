function entrar() {
    const user = document.getElementById('user').value;
    const pass = document.getElementById('pass').value;

    // Limpar erro anterior ao tentar novamente
    document.getElementById('erro').style.display = 'none';

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    })
    .then(res => {
        // O res.ok verifica se o status está entre 200-299
        return res.json();
    })
    .then(data => {
        if (data.ok) {
            // Sucesso total
            window.location.href = '/index';
        } else {
            // Credenciais inválidas (status 401 vindo do Python)
            exibirErro();
        }
    })
    .catch(err => {
        // Erro de rede ou servidor fora do ar
        console.error("Erro na requisição:", err);
        exibirErro();
    });
}

function exibirErro() {
    document.getElementById('erro').style.display = 'block';
}