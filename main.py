"""
main.py
--------
Servicio Flask que expone POST /scrape
y devuelve los comentarios de un video de TikTok en JSON.
"""

from __future__ import annotations

import os

from flask import Flask, jsonify, request
from scraper import fetch_comments

app = Flask(__name__)

# (Opcional) Permite redefinir tokens al arrancar
if os.getenv("MS_TOKEN"):
    os.environ["MS_TOKEN"] = os.getenv("MS_TOKEN")  # type: ignore
if os.getenv("DEVICE_ID"):
    os.environ["DEVICE_ID"] = os.getenv("DEVICE_ID")  # type: ignore


@app.post("/scrape")
def scrape():
    """Devuelve { "comments": [...] } o un error."""
    data = request.get_json(silent=True) or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "falta campo 'url'"}), 400

    try:
        comments = fetch_comments(url)
        return jsonify({"comments": comments})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    # Escucha en 0.0.0.0:8000 (puerto que configuraremos en EasyPanel)
    app.run(host="0.0.0.0", port=8000)
