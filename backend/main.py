from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import string
import random

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "urls.db"

# -------------------------
# Initialize database
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT UNIQUE,
            short_code TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

init_db()

class URLRequest(BaseModel):
    url: str

# -------------------------
# Generate short code
# -------------------------
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# -------------------------
# Shorten URL
# -------------------------
@app.post("/shorten")
def shorten_url(request: URLRequest, req: Request):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check if URL already exists
    cursor.execute("SELECT short_code FROM urls WHERE long_url=?", (request.url,))
    result = cursor.fetchone()

    host = req.headers.get("host")

    if result:
        conn.close()
        return {"short_url": f"http://{host}/{result[0]}"}

    short_code = generate_short_code()

    cursor.execute(
        "INSERT INTO urls (long_url, short_code) VALUES (?, ?)",
        (request.url, short_code)
    )
    conn.commit()
    conn.close()

    return {"short_url": f"http://{host}/{short_code}"}

# -------------------------
# Redirect Endpoint
# -------------------------
@app.get("/{short_code}")
def redirect_url(short_code: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT long_url FROM urls WHERE short_code=?", (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return RedirectResponse(result[0])
    else:
        raise HTTPException(status_code=404, detail="URL not found")
