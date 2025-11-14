from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask uygulamasını başlat
app = Flask(__name__)
# CORS'u etkinleştir
CORS(app)



def connect_db():
    """PostgreSQL veritabanına bağlantı kurar."""
    return psycopg2.connect(DATABASE_URL)


@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    """
    POST: Yeni ziyaretçi ekler.
    GET: Son 10 ziyaretçiyi listeler.
    """
    conn = connect_db()
    cur = conn.cursor()

    # Eğer yoksa ziyaretciler tablosunu oluştur
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        # POST isteği: Yeni isim ekle
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()
    
    # GET isteği veya POST sonrası dönüş: Son 10 ismi getir
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]
    
    # Bağlantıyı kapat
    cur.close()
    conn.close()
    
    return jsonify(isimler)


if __name__ == "__main__":
    # Uygulamayı 0.0.0.0 adresi ve 5001 portu üzerinden çalıştır
    app.run(host="0.0.0.0", port=5001)
