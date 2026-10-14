import os
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "host.docker.internal"),
        user=os.environ.get("DB_USER", "app_user"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "praktikum_db"),
        port=int(os.environ.get("DB_PORT", "3306")),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


@app.route("/")
def hello():
    return "Halo dari Flask + Docker + Jenkins!"


@app.route("/db")
def db_status():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS version")
            row = cur.fetchone()
        conn.close()
        return jsonify(status="terhubung", mysql_version=row["version"])
    except Exception as e:
        return jsonify(status="gagal", error=str(e)), 500


@app.route("/mahasiswa", methods=["GET"])
def list_mahasiswa():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, nama, created_at FROM mahasiswa ORDER BY id")
            rows = cur.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify(status="gagal", error=str(e)), 500


@app.route("/mahasiswa", methods=["POST"])
def add_mahasiswa():
    data = request.get_json(silent=True) or {}
    nama = data.get("nama", "").strip()
    if not nama:
        return jsonify(error="field 'nama' wajib diisi"), 400
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO mahasiswa (nama) VALUES (%s)", (nama,))
        conn.commit()
        conn.close()
        return jsonify(status="ditambahkan", nama=nama), 201
    except Exception as e:
        return jsonify(status="gagal", error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
