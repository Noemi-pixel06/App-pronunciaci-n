from flask import Flask, render_template, request, jsonify
from difflib import SequenceMatcher
import random
import sqlite3

app = Flask(__name__)

# ------------------ FRASES ------------------

frases = {
    "facil": ["Hola", "Buenos días", "Buenas tardes", "el gato", "hola como estas", "buenas noches"],
    "medio": ["quiero aprender español", "mañana iremos al parque", "el cielo es muy azul"],
    "dificil": ["los libros son mis amigos", "tengo un perro muy jugueton", "la vida es bella y divertida"]
}

# ------------------ BASE DE DATOS ------------------

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS puntajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        puntaje REAL
    )
    """)

    conn.commit()
    conn.close()

def guardar_puntaje(nombre, puntaje):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)",
        (nombre, puntaje)
    )

    conn.commit()
    conn.close()

def obtener_top3():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre, puntaje
        FROM puntajes
        ORDER BY puntaje DESC
        LIMIT 3
    """)

    top3 = cursor.fetchall()
    conn.close()
    return top3

# ------------------ LÓGICA ------------------

def evaluar_pronunciacion(original, dicho):
    similitud = SequenceMatcher(None, original, dicho).ratio()
    return round(similitud * 100, 2)

# ------------------ RUTAS ------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/frase", methods=["POST"])
def frase():
    nivel = request.form.get("nivel", "facil")
    frase = random.choice(frases.get(nivel, frases["facil"]))

    return jsonify({"frase": frase})

@app.route("/evaluar", methods=["POST"])
def evaluar():
    frase = request.form.get("frase", "")
    dicho = request.form.get("dicho", "").lower()
    nombre = request.form.get("nombre", "Anónimo")

    porcentaje = evaluar_pronunciacion(frase, dicho)

    guardar_puntaje(nombre, porcentaje)
    top3 = obtener_top3()

    return jsonify({
        "dicho": dicho,
        "porcentaje": porcentaje,
        "top3": top3
    })

# ------------------ INICIO ------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
