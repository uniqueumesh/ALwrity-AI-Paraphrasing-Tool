"""
AssemblyAI Text-to-Speech service helper for Streamlit.

Provides a single function `fetch_tts_mp3` that returns MP3 bytes for given text.
Falls back gracefully (returns None) on errors so caller can use browser TTS.
"""
from __future__ import annotations

import os
import hashlib
import json
from typing import Optional

import requests
import streamlit as st


def _hash_text_settings(text: str, voice: Optional[str]) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    h.update((voice or "").encode("utf-8"))
    return h.hexdigest()


@st.cache_data(show_spinner=False)
def fetch_tts_mp3(text: str, voice: Optional[str] = None) -> Optional[bytes]:
    """
    Fetch MP3 bytes for the given text using AssemblyAI TTS.

    - Caches by (text, voice) content hash
    - Returns None if API key missing or provider errors
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key or not text or not text.strip():
        return None

    # Safety: cap length to avoid excessive cost; trim if needed
    safe_text = text.strip()
    if len(safe_text) > 5000:
        safe_text = safe_text[:5000]

    # Basic request payload; adjust voice if you have preferred one configured
    payload = {
        "text": safe_text,
        # Replace with a valid AssemblyAI voice ID if you have one; leave None to use default
        **({"voice": voice} if voice else {}),
        # Other optional params could include format, sample_rate, speed, etc.
    }

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    try:
        # AssemblyAI TTS typically responds with an audio_url; some plans may return bytes directly.
        # Endpoint path may vary depending on account/feature; this is the common public form.
        resp = requests.post(
            "https://api.assemblyai.com/v2/tts",
            headers=headers,
            data=json.dumps(payload),
            timeout=30,
        )
        if not resp.ok:
            return None
        data = resp.json()

        # Prefer direct audio_url if provided, else try raw content if any
        audio_url = data.get("audio_url") or data.get("audioUrl")
        if audio_url:
            audio_resp = requests.get(audio_url, timeout=60)
            if audio_resp.ok and audio_resp.content:
                return audio_resp.content
            return None

        # Some responses can include base64 or bytes; check common fields
        if "audio_content" in data:
            try:
                import base64
                return base64.b64decode(data["audio_content"])  # type: ignore[arg-type]
            except Exception:
                return None

        # If none matched, return None to allow browser TTS fallback
        return None
    except Exception:
        return None


