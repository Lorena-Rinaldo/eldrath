from flask import Flask, render_template, jsonify, session, request
import requests
import random

app = Flask(__name__)
app.secret_key = "segredo-super-seguro"

BASE_URL = "https://www.dnd5eapi.co/api/2014"

headers = {"Accept": "application/json"}


def criar_personagem_padrao():
    return {"hp": 20, "ataque": 10, "defesa": 10, "arma": None, "nível": 1}


# =========================
# Dicionários de Tradução
# =========================

TRADUCOES_TIPO = {
    "aberration": "Aberração",
    "beast": "Fera",
    "celestial": "Celestial",
    "construct": "Constructo",
    "dragon": "Dragão",
    "elemental": "Elemental",
    "fey": "Feérico",
    "fiend": "Ínfero",
    "giant": "Gigante",
    "humanoid": "Humanoide",
    "monstrosity": "Monstruosidade",
    "ooze": "Lodo",
    "plant": "Planta",
    "undead": "Morto-vivo",
    "swarm": "Enxame",
}

TRADUCOES_TAMANHO = {
    "tiny": "Minúsculo",
    "small": "Pequeno",
    "medium": "Médio",
    "large": "Grande",
    "huge": "Enorme",
    "gargantuan": "Colossal",
}

TRADUCOES_ALINHAMENTO = {
    "lawful good": "Leal e Bom",
    "neutral good": "Neutro e Bom",
    "chaotic good": "Caótico e Bom",
    "lawful neutral": "Leal e Neutro",
    "neutral": "Neutro",
    "chaotic neutral": "Caótico e Neutro",
    "lawful evil": "Leal e Mau",
    "neutral evil": "Neutro e Mau",
    "chaotic evil": "Caótico e Mau",
    "unaligned": "Sem alinhamento",
    "any alignment": "Qualquer alinhamento",
}


def pegar_monstro():
    try:
        lista_response = requests.get(f"{BASE_URL}/monsters", headers=headers)
        lista = lista_response.json()["results"]
        escolhido = random.choice(lista)

        detalhe = requests.get(
            f"{BASE_URL}/monsters/{escolhido['index']}", headers=headers
        ).json()

        # Tradução Robusta (converte para lower antes de buscar)
        tipo_original = detalhe.get("type", "").lower()
        tamanho_original = detalhe.get("size", "").lower()
        alinhamento_original = detalhe.get("alignment", "").lower()

        return {
            "name": detalhe.get("name"),
            "size": TRADUCOES_TAMANHO.get(tamanho_original, detalhe.get("size")),
            "type": TRADUCOES_TIPO.get(tipo_original, detalhe.get("type")),
            "alignment": TRADUCOES_ALINHAMENTO.get(
                alinhamento_original, detalhe.get("alignment")
            ),
            "hp": detalhe.get("hit_points"),
            "cr": detalhe.get("challenge_rating"),
        }
    except Exception as e:
        print(f"Erro ao buscar  monstro: {e}")
        return None

# =========================
# Rotas
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/jogo")
def jogo():
    session["personagem"] = criar_personagem_padrao()
    session["monstro"] = pegar_monstro()
    return render_template("jogo.html", monstro=session["monstro"], cena=1)


@app.route("/jogo/<int:cena>")
def cenas(cena):
    if "personagem" not in session or "ataque" not in session["personagem"]:
        session["personagem"] = criar_personagem_padrao()

    if (
        "monstro" not in session
        or isinstance(session["monstro"].get("type"), str)
        and session["monstro"]["type"].islower()
    ):
        session["monstro"] = pegar_monstro()

    return render_template("jogo.html", cena=cena, monstro=session["monstro"])


@app.route("/api/equipar-arma", methods=["POST"])
def equipar_arma():
    if "personagem" not in session:
        session["personagem"] = criar_personagem_padrao()

    personagem = session["personagem"]
    personagem["arma"] = "Espada Longa"
    session["personagem"] = personagem  # Salva de volta na sessão
    return {"status": "ok"}


# =========================
# Rotas de cenas
# =========================


@app.route("/api/fugir", methods=["POST"])
def fugir():

    if "personagem" not in session:
        session["personagem"] = criar_personagem_padrao()

    dado = random.randint(1, 20)

    sucesso = dado >= 10

    if not sucesso:
        session["personagem"]["hp"] -= 5

    return {"dado": dado, "sucesso": sucesso, "hp": session["personagem"]["hp"]}


# =========================
# Run
# =========================

if __name__ == "__main__":
    app.run(debug=True)
