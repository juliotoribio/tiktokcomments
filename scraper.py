"""
scraper.py
-----------
Funciones para extraer todos los comentarios de un video de TikTok.
"""

from __future__ import annotations
import json
import logging
import os
import time
from typing import List

import requests

# Logging básico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cabeceras para simular un navegador real
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.tiktok.com/explore",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/129.0.0.0 Safari/537.36"
    )
}

# Lee tokens de variables de entorno
MS_TOKEN: str | None = os.getenv("MS_TOKEN")
DEVICE_ID: str | None = os.getenv("DEVICE_ID")


def fetch_comments(post_url: str) -> List[str]:
    """
    Descarga todos los comentarios de un video.

    Parameters
    ----------
    post_url : str
        URL completa del video de TikTok.

    Returns
    -------
    list[str]
        Lista de comentarios.
    """
    if not MS_TOKEN or not DEVICE_ID:
        raise RuntimeError(
            "MS_TOKEN o DEVICE_ID no definidos como variables de entorno."
        )

    post_id = post_url.rstrip("/").split("/")[-1]
    comments: List[str] = []
    cursor = 0

    while True:
        url = (
            "https://www.tiktok.com/api/comment/list/"
            f"?aid=1988&app_name=tiktok_web&aweme_id={post_id}"
            "&count=20"
            f"&cursor={cursor}"
            f"&device_id={DEVICE_ID}"
            f"&msToken={MS_TOKEN}"
        )

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, json.JSONDecodeError) as err:
            logging.error("Error al obtener comentarios: %s", err)
            break

        # Extraer texto de cada comentario
        for cm in data.get("comments", []):
            text = cm.get("share_info", {}).get("desc") or cm.get("text")
            if text:
                comments.append(text)

        # Verificar si hay más páginas
        if data.get("has_more") != 1:
            break

        cursor += 20
        time.sleep(1)  # pausa para no exceder rate-limit

    return comments
