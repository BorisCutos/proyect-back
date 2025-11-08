from flask import Flask, jsonify
import os, psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mydb-postgresql")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "openshift")
DB_PASSWORD = os.getenv("DB_PASSWORD", "openshift")
DB_NAME = os.getenv("DB_NAME", "proj-openshift")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )

def ensure_schema():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
              CREATE TABLE IF NOT EXISTS items(
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
              );
            """)
            cur.execute("SELECT COUNT(*) FROM items;")
            if cur.fetchone()[0] == 0:
                cur.executemany("INSERT INTO items(name) VALUES (%s)", [("alpha",), ("beta",), ("gamma",)])

@app.get("/items")
def items():
    try:
        ensure_schema()
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM items ORDER BY id;")
                rows = cur.fetchall()
        return jsonify([{"id": r[0], "name": r[1]} for r in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/startup")
def startup(): return ("OK", 200)

@app.get("/readiness")
def readiness():
    try:
        with get_conn():
            pass
        return ("OK", 200)
    except Exception:
        return ("DB_NOT_READY", 503)

@app.get("/health")
def health(): return ("OK", 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
