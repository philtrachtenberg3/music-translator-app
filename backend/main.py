from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import re
from typing import List, Dict, Optional
import unicodedata

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

class SongRequest(BaseModel):
    artist: str
    title: str
    source_language: str = "ES"  # Default to Spanish
    target_language: str = "EN-US"  # Default to English

class TranslationRequest(BaseModel):
    spanish_text: str
    source_language: str = "ES"  # Default to Spanish
    target_language: str = "EN-US"  # Default to English

class WordAlignment(BaseModel):
    spanish: str
    english: str

class TranslationResponse(BaseModel):
    status: str = "ok"  # "ok" or "not_found"
    spanish_lyrics: str
    english_lyrics: str
    word_pairs: List[WordAlignment]
    detected_language: str
    audio_url: Optional[str] = None
    fallback_url: Optional[str] = None
    message: Optional[str] = None

def _strip_diacritics(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

def _strip_features(title: str) -> str:
    return re.sub(r'[\(\[]\s*(feat\.?|with|con|remix|version|vers\.)[^)\]]*[\)\]]', '', title, flags=re.I).strip()

def get_lyrics_from_lyrics_ovh(artist: str, title: str) -> Optional[str]:
    variants = [
        (artist, title),
        (artist, _strip_features(title)),
        (_strip_diacritics(artist), _strip_diacritics(title)),
        (_strip_diacritics(artist), _strip_diacritics(_strip_features(title))),
    ]

    for a, t in variants:
        if not a or not t:
            continue
        url = f"https://api.lyrics.ovh/v1/{requests.utils.quote(a)}/{requests.utils.quote(t)}"
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                data = r.json()
                lyr = (data.get("lyrics") or "").strip()
                if lyr:
                    return lyr
        except requests.RequestException:
            continue

    return None

def get_genius_song_url(artist: str, title: str) -> Optional[str]:
    """Genius API lookup for a song URL (NO scraping)."""
    if not GENIUS_API_TOKEN:
        return None
    try:
        headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
        search_url = "https://api.genius.com/search"
        params = {"q": f"{title} {artist}"}
        r = requests.get(search_url, params=params, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        hits = data.get("response", {}).get("hits", [])
        if not hits:
            return None
        return hits[0]["result"]["url"]
    except Exception as e:
        print(f"Error getting Genius URL: {e}")
        return None

def detect_language(text: str) -> str:
    """
    Detect if text is in Spanish or English based on common words.
    Returns 'ES' or 'EN-US'
    """
    try:
        text_lower = text.lower()
        
        # Common Spanish words
        spanish_words = {'el', 'la', 'de', 'que', 'y', 'en', 'un', 'una', 'es', 'está', 'son', 'estar', 'me', 'te', 'se', 'más', 'como', 'para', 'con', 'pero', 'si', 'sí'}
        
        # Common English words
        english_words = {'the', 'and', 'is', 'are', 'to', 'in', 'of', 'a', 'that', 'it', 'for', 'be', 'you', 'with', 'have', 'this', 'but', 'as', 'or', 'from'}
        
        # Count matches
        spanish_count = len([word for word in spanish_words if word in text_lower])
        english_count = len([word for word in english_words if word in text_lower])
        
        # Return the detected language
        if english_count > spanish_count:
            return 'EN-US'
        else:
            return 'ES'
    except:
        return 'ES'  # Default to Spanish

def translate_with_deepl(text: str, source_lang: str = "ES", target_lang: str = "EN-US") -> str:
    """Translate text using DeepL API"""
    try:
        if not DEEPL_API_KEY:
            print("DeepL API key not set, using fallback translation")
            return translate_fallback(text, source_lang, target_lang)
        
        url = "https://api-free.deepl.com/v1/translate"
        
        params = {
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "source_language": source_lang,
            "target_language": target_lang,
        }
        
        response = requests.post(url, data=params, timeout=10)
        
        if response.status_code == 403:
            print("DeepL API key invalid or unauthorized. Using fallback translation.")
            return translate_fallback(text, source_lang, target_lang)
        
        response.raise_for_status()
        data = response.json()
        
        return data["translations"][0]["text"]
    
    except Exception as e:
        print(f"Error with DeepL translation: {e}")
        print("Using fallback translation service...")
        # Fallback to simple translation
        return translate_fallback(text, source_lang, target_lang)

def translate_fallback(text: str, source_lang: str = "ES", target_lang: str = "EN-US") -> str:
    """Fallback translation using Google Translate free API"""
    try:
        print(f"[FALLBACK] Using Google Translate free API...")
        
        # Map DeepL language codes to Google Translate codes
        lang_map = {
            'ES': 'es',
            'EN-US': 'en',
            'EN': 'en',
            'PT-BR': 'pt',
            'PT': 'pt',
            'FR': 'fr',
            'DE': 'de',
            'IT': 'it',
            'NL': 'nl',
            'PL': 'pl',
            'RU': 'ru',
            'JA': 'ja',
            'ZH': 'zh-CN',
            'KO': 'ko',
            'TR': 'tr',
        }
        
        source = lang_map.get(source_lang, 'es')
        target = lang_map.get(target_lang, 'en')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Use the free Google Translate API
        params = {
            'client': 'gtx',
            'sl': source,
            'tl': target,
            'dt': 't',
            'q': text
        }
        
        response = requests.get('https://translate.googleapis.com/translate_a/single', params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                result = response.json()
                # The translation is in the first element of the first array
                if result and result[0]:
                    translated = ''.join([item[0] for item in result[0] if item[0]])
                    print(f"[FALLBACK] Translation successful!")
                    return translated
            except:
                pass
        
        print(f"[FALLBACK] Google Translate failed, returning original text")
        return text
        
    except Exception as e:
        print(f"[FALLBACK] Error: {e}")
        return text

def align_words(spanish_text: str, english_text: str) -> List[WordAlignment]:
    """
    Align Spanish and English lines for accurate comparison.
    Uses line-by-line alignment instead of word-by-word for much better accuracy.
    """
    try:
        spanish_lines = [line.strip() for line in spanish_text.split('\n') if line.strip()]
        english_lines = [line.strip() for line in english_text.split('\n') if line.strip()]
        
        # Pair up lines - this is much more accurate than word-by-word
        pairs = []
        min_length = min(len(spanish_lines), len(english_lines))
        
        for i in range(min_length):
            # Only add non-empty line pairs
            if spanish_lines[i] and english_lines[i]:
                pairs.append(WordAlignment(
                    spanish=spanish_lines[i],
                    english=english_lines[i]
                ))
        
        return pairs
    except Exception as e:
        print(f"Error aligning lines: {e}")
        return []

def get_spotify_audio_url(artist: str, title: str) -> Optional[str]:
    """Get Spotify preview URL for a song"""
    try:
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            return None
        
        # Get access token
        auth_url = "https://accounts.spotify.com/api/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }
        
        auth_response = requests.post(auth_url, data=auth_data, timeout=10)
        auth_response.raise_for_status()
        access_token = auth_response.json()["access_token"]
        
        # Search for song
        search_url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "q": f"track:{title} artist:{artist}",
            "type": "track",
            "limit": 1
        }
        
        search_response = requests.get(search_url, headers=headers, params=params, timeout=10)
        search_response.raise_for_status()
        results = search_response.json()
        
        if results["tracks"]["items"]:
            preview_url = results["tracks"]["items"][0].get("preview_url")
            return preview_url
        
        return None
    
    except Exception as e:
        print(f"Error getting Spotify audio: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Music Translation API is running"}

@app.post("/translate-song", response_model=TranslationResponse)
def translate_song(request: SongRequest):
    try:
        # 1) Try lyrics.ovh first (safe + fast)
        lyrics = get_lyrics_from_lyrics_ovh(request.artist, request.title)

        # 2) If not found, return a clean fallback payload (200 OK)
        if not lyrics:
            genius_url = get_genius_song_url(request.artist, request.title) \
                or f"https://genius.com/search?q={requests.utils.quote(request.artist + ' ' + request.title)}"

            audio_url = get_spotify_audio_url(request.artist, request.title)

            return TranslationResponse(
                status="not_found",
                spanish_lyrics="",
                english_lyrics="",
                word_pairs=[],
                detected_language="",
                audio_url=audio_url,
                fallback_url=genius_url,
                message="Lyrics not available from supported sources. Open the Genius link or paste lyrics to translate."
            )

        # 3) Detect language and translate
        detected_lang = detect_language(lyrics)
        translated_lyrics = translate_with_deepl(
            lyrics,
            source_lang=detected_lang,
            target_lang=request.target_language
        )

        word_pairs = align_words(lyrics, translated_lyrics)
        audio_url = get_spotify_audio_url(request.artist, request.title)

        return TranslationResponse(
            status="ok",
            spanish_lyrics=lyrics,
            english_lyrics=translated_lyrics,
            word_pairs=word_pairs,
            detected_language=detected_lang,
            audio_url=audio_url
        )

    except Exception as e:
        print(f"Error in translate_song: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate-text")
def translate_text(request: TranslationRequest):
    """
    Translate manually pasted text to selected language (auto-detects source language)
    """
    try:
        spanish_text = request.spanish_text
        
        if not spanish_text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Auto-detect the language of the text
        detected_lang = detect_language(spanish_text)
        
        # Translate to selected target language from detected language
        translated_text = translate_with_deepl(spanish_text, source_lang=detected_lang, target_lang=request.target_language)
        
        # Align lines
        word_pairs = align_words(spanish_text, translated_text)
        
        return {
            "spanish_lyrics": spanish_text,
            "english_lyrics": translated_text,
            "word_pairs": word_pairs,
            "detected_language": detected_lang
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in translate_text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)