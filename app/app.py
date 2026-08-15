import os
import random
import string
from datetime import datetime, timezone

import mysql.connector
import redis
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "urluser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "urlshortener")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

cache = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)


def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    original_url = data["url"]
    short_code = generate_code()

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO urls (original_url, short_code, created_at, click_count)
        VALUES (%s, %s, %s, %s)
        """,
        (original_url, short_code, datetime.now(timezone.utc), 0)
    )

    db.commit()
    cursor.close()
    db.close()

    return jsonify({
        "original_url": original_url,
        "short_url": f"/{short_code}",
        "short_code": short_code
    })


@app.route("/<short_code>")
def redirect_url(short_code):

    cached_url = cache.get(short_code)

    if cached_url:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code = %s",
            (short_code,)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect(cached_url)

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM urls WHERE short_code = %s",
        (short_code,)
    )

    result = cursor.fetchone()

    if not result:
        cursor.close()
        db.close()
        return jsonify({"error": "URL not found"}), 404

    cursor.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code = %s",
        (short_code,)
    )

    db.commit()

    cache.set(short_code, result["original_url"])

    cursor.close()
    db.close()

    return redirect(result["original_url"])


@app.route("/stats/<short_code>")
def stats(short_code):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM urls WHERE short_code = %s",
        (short_code,)
    )

    result = cursor.fetchone()

    cursor.close()
    db.close()

    if not result:
        return jsonify({"error": "URL not found"}), 404

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 

