# 🎵 Music Translation App

A full-stack web application for translating Spanish song lyrics to English with side-by-side comparison, word-by-word translations, and audio playback.

## Features

✨ **Core Features:**
- 🎯 Side-by-side Spanish/English lyrics comparison (priority feature)
- 📖 Word-by-word translation alignment
- 🎧 Audio preview playback
- 🔍 Search songs by artist and title
- 📋 Paste and translate manual lyrics
- 🎨 Beautiful, responsive UI

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env`
3. Add your API keys to `.env`
4. Follow the QUICKSTART.md

## Tech Stack

**Backend:**
- Python FastAPI
- Genius API (lyrics)
- DeepL API (translation, or MyMemory fallback)
- Spotify API (audio playback)

**Frontend:**
- React 18
- CSS3 with responsive design

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- Git

## API Keys Required

### 1. Genius API (Required)
1. Go to https://genius.com/api-clients
2. Create an account if needed
3. Create a new API Client
4. Copy your access token
5. This will be your `GENIUS_API_TOKEN`

### 2. DeepL API (Recommended)
1. Go to https://www.deepl.com/pro-api
2. Sign up for a free account (500,000 characters/month free)
3. Copy your API key from the dashboard
4. This will be your `DEEPL_API_KEY`

(If you don't have DeepL, the app will fall back to MyMemory API, which is free but lower quality)

### 3. Spotify API (Optional, for audio preview)
1. Go to https://developer.spotify.com/dashboard
2. Create an app
3. Copy your Client ID and Client Secret
4. These will be your `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`

## Installation

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor
```

Edit `.env` file:
```
GENIUS_API_TOKEN=your_token_here
DEEPL_API_KEY=your_key_here
SPOTIFY_CLIENT_ID=your_id_here
SPOTIFY_CLIENT_SECRET=your_secret_here
```

### Start Backend

```bash
# Make sure you're in backend directory and venv is activated
python main.py
```

The backend will start at `http://localhost:8000`

### Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

The frontend will start at `http://localhost:3000` and automatically open in your browser.

## Usage

### Option 1: Search for a Song
1. Enter the artist name (e.g., "Juan Luis Guerra")
2. Enter the song title (e.g., "Ojalá que llueva café")
3. Click "Search & Translate"
4. See results with:
   - Side-by-side lyrics comparison
   - Word-by-word translations
   - Audio preview (if available)

### Option 2: Paste Lyrics Manually
1. Switch to "Paste Lyrics" tab
2. Paste your Spanish lyrics
3. Click "Translate"
4. See all the same results as above

## Project Structure

```
music-translation-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Example environment variables
│   └── .env                  # Your API keys (git ignored)
└── frontend/
    ├── src/
    │   ├── App.jsx           # Main React component
    │   ├── App.css           # Styling
    │   └── ...
    ├── package.json
    └── .env                  # Frontend config
```

## How It Works

1. **User Input**: User searches for a song or pastes lyrics
2. **Backend Processing**:
   - Fetches Spanish lyrics from Genius API
   - Translates to English using DeepL (or MyMemory fallback)
   - Aligns words for comparison
   - Fetches Spotify audio URL
3. **Frontend Display**: Shows results with all features
4. **User Interaction**: Can search new songs or clear and start over

## Customization

### Improving Word Alignment
Currently uses simple word-pair matching. For better alignment, consider:
- Using alignment libraries: `alignment`, `textdistance`
- Using translation APIs that support word-level data (e.g., Google Translate Cloud)
- Implementing more sophisticated NLP algorithms

### Better Translation Quality
- DeepL provides better translations than MyMemory
- For contextual/cultural understanding, consider using GPT APIs
- Can add professional translation mode with multiple providers

### Additional Features to Add
1. Save/bookmark favorite translations
2. Export to PDF with formatting
3. Karaoke mode (highlighting lyrics as they play)
4. Multiple language support
5. Offline mode with downloaded songs
6. User authentication and saved history

## Troubleshooting

### "Lyrics not found"
- Try different spelling of artist/song names
- Make sure the song exists on Genius
- Try searching on https://genius.com directly first

### Translation errors
- Check that DeepL API key is valid and has quota remaining
- The app will automatically fall back to MyMemory if DeepL fails
- MyMemory has daily limits; refresh or wait

### Audio not playing
- Not all songs have preview URLs on Spotify
- Spotify preview URLs are 30-second clips
- Some songs may have licensing restrictions

### Backend connection errors
- Ensure backend is running on http://localhost:8000
- Check that `REACT_APP_API_URL` is set correctly in frontend/.env
- Try clearing browser cache
- Check CORS settings in main.py

## Production Deployment

### Backend
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000

# Or using gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend
```bash
# Build for production
npm run build

# Deploy the 'build' folder to your hosting service
# (Netlify, Vercel, GitHub Pages, etc.)
```

### Environment Variables for Production
- Store API keys in secure environment variables (not .env files)
- Use production API endpoints for each service
- Set `REACT_APP_API_URL` to your backend deployment URL

## API Reference

### Backend Endpoints

#### Search and Translate Song
```
POST /translate-song
Content-Type: application/json

{
  "artist": "Juanes",
  "title": "La Camisa Negra"
}

Response:
{
  "spanish_lyrics": "...",
  "english_lyrics": "...",
  "word_pairs": [...],
  "audio_url": "https://..."
}
```

#### Translate Manual Text
```
POST /translate-text
Content-Type: application/json

{
  "spanish_text": "..."
}

Response:
{
  "spanish_lyrics": "...",
  "english_lyrics": "...",
  "word_pairs": [...]
}
```

## License

MIT License - feel free to use and modify!

## Contributing

Contributions are welcome! Areas for improvement:
- Better word alignment algorithms
- Support for more languages
- Caching/database for frequently searched songs
- User accounts and preferences
- Mobile app (React Native)

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation for each service
3. Check backend logs for errors
4. Check browser console for frontend errors

## Notes

- Genius stores lyrics as user-contributed content under their Terms of Service
- Lyrics are fetched on-demand and displayed for educational purposes
- Spotify API provides 30-second preview clips
- Translation quality depends on the API provider
- Respect copyright and terms of service for all APIs used

---

Enjoy translating your favorite Spanish songs! 🎵
