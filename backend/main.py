from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import re
from typing import List, Dict, Optional

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

class TranslationRequest(BaseModel):
    spanish_text: str

class WordAlignment(BaseModel):
    spanish: str
    english: str

class WordTranslation(BaseModel):
    word: str
    translation: str
    line_index: int

class TranslationResponse(BaseModel):
    spanish_lyrics: str
    english_lyrics: str
    word_pairs: List[WordAlignment]
    word_translations: List[WordTranslation]
    audio_url: Optional[str] = None

def get_lyrics_from_genius(artist: str, title: str) -> Optional[str]:
    """Fetch lyrics from Genius API"""
    try:
        headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
        search_url = "https://api.genius.com/search"
        params = {"q": f"{title} {artist}"}
        
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data["response"]["hits"]:
            return None
        
        # Get the first matching song
        song_url = data["response"]["hits"][0]["result"]["url"]
        
        # Fetch the lyrics page
        page_response = requests.get(song_url, timeout=10)
        page_response.raise_for_status()
        
        # Parse HTML to extract lyrics
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_response.content, 'html.parser')
        
        # Genius stores lyrics in div tags with data-lyrics-container attribute
        lyrics_divs = soup.find_all('div', {'data-lyrics-container': 'true'})
        
        if not lyrics_divs:
            return None
        
        # Extract lyrics while preserving line breaks
        all_lyrics = []
        for div in lyrics_divs:
            # Get text and preserve line breaks from <br> tags
            for br in div.find_all('br'):
                br.replace_with('\n')
            text = div.get_text()
            all_lyrics.append(text)
        
        lyrics = "\n".join(all_lyrics)
        
        # Clean up common Genius metadata patterns
        # Remove lines that look like "XX ContributorsDate La Vuelta Lyrics..."
        lines = lyrics.split('\n')
        cleaned_lines = []
        for line in lines:
            # Skip lines that start with numbers followed by "Contributors" or "Lyrics"
            if not (line and line[0].isdigit() and ('Contributors' in line or 'Letra de' in line or 'Lyrics' in line)):
                cleaned_lines.append(line)
        
        lyrics = '\n'.join(cleaned_lines).strip()
        return lyrics
    
    except Exception as e:
        print(f"Error fetching lyrics from Genius: {e}")
        return None

def translate_with_deepl(text: str, source_lang: str = "ES", target_lang: str = "EN-US") -> str:
    """Translate text using DeepL API"""
    try:
        if not DEEPL_API_KEY:
            print("DeepL API key not set, using fallback translation")
            return translate_fallback(text)
        
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
            return translate_fallback(text)
        
        response.raise_for_status()
        data = response.json()
        
        return data["translations"][0]["text"]
    
    except Exception as e:
        print(f"Error with DeepL translation: {e}")
        print("Using fallback translation service...")
        # Fallback to simple translation
        return translate_fallback(text)

def translate_fallback(text: str) -> str:
    """Fallback translation using Google Translate free API"""
    try:
        print(f"[FALLBACK] Using Google Translate free API...")
        
        # Use Google Translate free endpoint
        from urllib.parse import quote
        url = f"https://translate.googleapis.com/translate_a/element.js?cb=googleTranslateElementInit"
        
        # Try a simpler approach with requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Use the free Google Translate API
        params = {
            'client': 'gtx',
            'sl': 'es',
            'tl': 'en',
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

def create_word_translations(spanish_text: str, english_text: str) -> List[WordTranslation]:
    """
    Create word-level translations by aligning Spanish and English lines.
    Returns a list mapping each Spanish word to its English translation.
    """
    try:
        spanish_lines = spanish_text.split('\n')
        english_lines = english_text.split('\n')
        
        word_translations = []
        
        # Process each line pair
        for line_idx, (sp_line, en_line) in enumerate(zip(spanish_lines, english_lines)):
            sp_line = sp_line.strip()
            en_line = en_line.strip()
            
            if not sp_line or not en_line:
                continue
            
            # Split into words
            sp_words = re.findall(r'\b\w+\b', sp_line.lower())
            en_words = re.findall(r'\b\w+\b', en_line.lower())
            
            # Simple alignment: pair words in order
            # This works reasonably well for most cases
            min_len = min(len(sp_words), len(en_words))
            
            for i in range(min_len):
                word_translations.append(WordTranslation(
                    word=sp_words[i],
                    translation=en_words[i],
                    line_index=line_idx
                ))
        
        return word_translations
    
    except Exception as e:
        print(f"Error creating word translations: {e}")
        return []

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
    """
    Main endpoint: fetch lyrics and translate them
    """
    try:
        # Fetch lyrics from Genius
        spanish_lyrics = get_lyrics_from_genius(request.artist, request.title)
        
        if not spanish_lyrics:
            raise HTTPException(status_code=404, detail="Lyrics not found on Genius")
        
        # Translate to English
        english_lyrics = translate_with_deepl(spanish_lyrics)
        
        # Align lines
        word_pairs = align_words(spanish_lyrics, english_lyrics)
        
        # Create word-level translations
        word_translations = create_word_translations(spanish_lyrics, english_lyrics)
        
        # Get Spotify audio URL
        audio_url = get_spotify_audio_url(request.artist, request.title)
        
        return TranslationResponse(
            spanish_lyrics=spanish_lyrics,
            english_lyrics=english_lyrics,
            word_pairs=word_pairs,
            word_translations=word_translations,
            audio_url=audio_url
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in translate_song: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate-text")
def translate_text(request: TranslationRequest):
    """
    Translate manually pasted Spanish text
    """
    try:
        spanish_text = request.spanish_text
        
        if not spanish_text:
            raise HTTPException(status_code=400, detail="Spanish text is required")
        
        # Translate to English
        english_text = translate_with_deepl(spanish_text)
        
        # Align lines
        word_pairs = align_words(spanish_text, english_text)
        
        # Create word-level translations
        word_translations = create_word_translations(spanish_text, english_text)
        
        return {
            "spanish_lyrics": spanish_text,
            "english_lyrics": english_text,
            "word_pairs": word_pairs,
            "word_translations": word_translations
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in translate_text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)