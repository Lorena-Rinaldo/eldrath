function animarDado(callbackFinal) {
    const valorSpan = document.getElementById("valor-dado");
    let animacao = setInterval(() => {
        valorSpan.textContent = Math.floor(Math.random() * 20) + 1;
    }, 80);

    setTimeout(() => {
        clearInterval(animacao);
        setTimeout(() => { callbackFinal(); }, 500);
    }, 1500);
}

function tentarFugir() {
    document.getElementById("cena3").classList.add("hidden");
    document.getElementById("cena4").classList.remove("hidden");

    animarDado(() => {
        fetch("/api/fugir", { method: "POST" })
            .then(r => r.json())
            .then(data => {
                const msg = document.getElementById("mensagemResultado");
                document.getElementById("valor-dado").textContent = data.dado;

                // ⭐ AQUI — logo após receber os dados
                if (!data.sucesso && data.hp !== undefined) {
                    atualizarHP(data.hp);
                }

                msg.textContent = data.sucesso
                    ? "🏃 Escapou!"
                    : "💥 Falhou! HP: " + data.hp;

                document.getElementById("telaResultado").classList.remove("hidden");
            });
    });
}

function equiparArma() {
    fetch("/api/equipar-arma", { method: "POST" })
        .then(() => { window.location.href = "/jogo/3"; });
}

function atualizarHP(novoHP) {
    const barra = document.getElementById("barra-hp");
    const textoHP = document.getElementById("texto-hp");

    if (barra) {
        barra.style.width = novoHP + "%";
    }

    if (textoHP) {
        textoHP.textContent = `${novoHP}/100`;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (typeof cenaAtual !== 'undefined' && cenaAtual === 4) {
        animarDado(() => {
            const valor = Math.floor(Math.random() * 20) + 1;
            document.getElementById("valor-dado").textContent = valor;
            const msg = document.getElementById("mensagemResultado");
            msg.textContent = valor >= 10 ? "⚔️ Acertou!" : "💀 Errou!";
            document.getElementById("telaResultado").classList.remove("hidden");
        });
    }
});