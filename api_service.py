from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os
from psycopg2 import pool

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")

# Connection pool
db_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)

def init_db():
    conn = db_pool.getconn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    db_pool.putconn(conn)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = db_pool.getconn()
    cur = conn.cursor()

    try:
        if request.method == "POST":
            isim = request.json.get("isim")
            if isim:
                cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
                conn.commit()

        cur.execute("SELECT id, isim, created_at FROM ziyaretciler ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        ziyaretci_listesi = [
            {"id": r[0], "isim": r[1], "created_at": r[2].isoformat()} for r in rows
        ]
        return jsonify(ziyaretci_listesi)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        db_pool.putconn(conn)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
