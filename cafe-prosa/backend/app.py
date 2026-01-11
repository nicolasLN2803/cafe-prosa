from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import bcrypt

app = Flask(__name__)
CORS(app)

DB = "database.db"
HASH_ADMIN = "$2b$12$4Zc72oNHSMX5hn0ZAxIjo.LcbH2DYeeqOm0h3aJcQ4OfyIHA82w7q"  # Exemplo de hash para a senha "admin123"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/contato", methods=["POST"])
def contato():
    dados = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)

    cursor.execute("""
        INSERT INTO mensagens (nome, email, mensagem, data)
        VALUES (?, ?, ?, ?)
    """, (
        dados.get("nome"),
        dados.get("email"),
        dados.get("mensagem"),
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "sucesso",
        "mensagem": "Mensagem enviada com sucesso!"
    })

@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    senha = request.headers.get("Authorization")

    if not senha:
        return jsonify({"erro": "Acesso não autorizado"}), 401

    # Ensure HASH_ADMIN is bytes for bcrypt.checkpw
    hash_admin_bytes = HASH_ADMIN.encode("utf-8") if isinstance(HASH_ADMIN, str) else HASH_ADMIN
    if not bcrypt.checkpw(senha.encode("utf-8"), hash_admin_bytes):
        return jsonify({"erro": "Acesso não autorizado"}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, mensagem, data FROM mensagens ORDER BY id DESC")
    rows = cursor.fetchall()
    mensagens = [dict(row) for row in rows]
    conn.close()

    return jsonify({"status": "sucesso", "mensagens": mensagens})


# Run server
if __name__ == "__main__":
    app.run()
