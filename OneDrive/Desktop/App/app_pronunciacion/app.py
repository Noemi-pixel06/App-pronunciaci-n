from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
import random

app = Flask(__name__)

# Frases por nivel
frases = {
    "facil": ["hola", "me gusta el color rosa", "el gato", "hola como estas", "buenos dias"],
    "medio": ["quiero aprender español", "mañana iremos al parque", "el cielo es muy azul"],
    "dificil": ["los libros son mis amigos", "tengo un perro muy jugueton", "la vida es bella y divertida"]
}

# Podio de puntajes (reinicia al cerrar la app)
podio = []

def evaluar_pronunciacion(original, dicho):
    similitud = SequenceMatcher(None, original, dicho).ratio()
    return round(similitud * 100, 2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/frase", methods=["POST"])
def frase():
    nivel = request.form["nivel"]
    frase = random.choice(frases[nivel])
    return jsonify({"frase": frase})

@app.route("/evaluar", methods=["POST"])
def evaluar():
    frase = request.form["frase"]
    dicho = request.form["dicho"].lower()
    porcentaje = evaluar_pronunciacion(frase, dicho)

    # Guardamos en podio
    podio.append(porcentaje)
    podio.sort(reverse=True)
    top3 = podio[:3]

    return jsonify({
        "dicho": dicho,
        "porcentaje": porcentaje,
        "top3": top3
    })

if __name__ == "__main__":
    app.run(debug=True)