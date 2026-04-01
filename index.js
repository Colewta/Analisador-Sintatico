async function analisar() {
    const codigo = document.getElementById('entrada').value;

    const div = document.getElementById('resultado');
    div.innerHTML = '';

    try {
        const res = await fetch('http://127.0.0.1:5000/analisar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo })
        });

        const data = await res.json();

        data.forEach(item => {
            const el = document.createElement('div');

            if (item.tipo === 'ERRO') {
                el.className = 'erro';
                el.innerText = `Erro na posição ${item.posicao}: ${item.valor}`;
            } else {
                el.className = 'sucesso';
                el.innerText = item.valor;
            }

            div.appendChild(el);
        });

    } catch (error) {
        const el = document.createElement('div');
        el.className = 'erro';
        el.innerText = 'Erro ao conectar com o servidor';
        div.appendChild(el);
    }
}