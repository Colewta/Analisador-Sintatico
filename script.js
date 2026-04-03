async function analisar() {
    const codigo = document.getElementById('codigo').value;
    const resultado = document.getElementById('resultado');

    resultado.innerHTML = '';

    try {
        const res = await fetch('http://127.0.0.1:5000/analisar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo })
        });

        const tokens = await res.json();

        tokens.forEach(t => {
            const div = document.createElement('div');

            div.className = `token ${t.tipo}`;
            div.innerText = `[${t.tipo}] "${t.valor}" (linha ${t.linha}, coluna ${t.coluna})`;

            resultado.appendChild(div);
        });

    } catch (err) {
        resultado.innerHTML = '<div class="ERRO">Erro ao conectar com servidor</div>';
    }
}