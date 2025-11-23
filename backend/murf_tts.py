# backend/murf_tts.py
from .config import MURF_API_KEY

def generate_audio(text):
    # If Murf key missing, return silent audio placeholder
    if not MURF_API_KEY:
        return b"\x00\x00\x00\x00"

    # TODO: add Murf later
    return b"\x00\x00\x00\x00"
