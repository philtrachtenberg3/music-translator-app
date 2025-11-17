# 🚀 Quick Start Guide

Get the music translation app running in 10 minutes!

## Step 1: Get API Keys (5 minutes)

### Genius API (Required)
1. Go to https://genius.com/api-clients
2. Log in or sign up
3. Click "Generate Access Token"
4. Copy the token (40+ character string)

### DeepL API (Recommended, Free Tier)
1. Go to https://www.deepl.com/pro-api
2. Click "Start for free"
3. Sign up (no credit card needed for free tier)
4. Go to your account page and copy your API key

### Spotify (Optional, for audio)
1. Go to https://developer.spotify.com/dashboard
2. Log in or sign up
3. Create an App
4. Accept the terms and create
5. Copy your Client ID and Client Secret

## Step 2: Set Up Backend (3 minutes)

```bash
# Open terminal/command prompt and navigate to the project folder

# Go to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
# On Windows, create a file named ".env" and add:
GENIUS_API_TOKEN=your_genius_token_here
DEEPL_API_KEY=your_deepl_key_here
SPOTIFY_CLIENT_ID=your_spotify_id
SPOTIFY_CLIENT_SECRET=your_spotify_secret

# Start the backend
python main.py
```

You should see: `Uvicorn running on http://127.0.0.1:8000`

**Leave this terminal running!**

## Step 3: Set Up Frontend (2 minutes)

Open a **NEW terminal** (keep backend running):

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# This will take 1-2 minutes...

# Start the app
npm start
```

The app will automatically open in your browser at `http://localhost:3000`

## Done! 🎉

Your app is now running! Try:
1. **Search Mode**: Enter "Juanes" and "La Camisa Negra" → Click Search & Translate
2. **Paste Mode**: Switch tab and paste some Spanish lyrics → Click Translate

You'll see:
- ✅ Side-by-side Spanish/English lyrics
- ✅ Word-by-word translations
- ✅ Audio preview (if available)

## Troubleshooting

### Backend won't start
- Make sure Python 3.8+ is installed: `python --version`
- Make sure venv is activated (you should see `(venv)` in terminal)
- Check that API keys in `.env` are correct

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` folder and run `npm install` again
- Try: `npm cache clean --force`

### "No lyrics found"
- Try a different song/artist spelling
- Check that the song exists on https://genius.com

### Translation errors
- Check your DeepL API key is correct
- If errors persist, app falls back to free MyMemory API (lower quality)

### API Key Issues
- **Genius**: Go to https://genius.com/api-clients and regenerate if needed
- **DeepL**: Check you used the free API endpoint (api-free.deepl.com)
- **Spotify**: Make sure Client Secret is correct (not visible after creation - regenerate if needed)

## Next Steps

Once working, check the main `README.md` for:
- Full feature documentation
- Customization options
- Deployment to the web
- Advanced setup

## Common Customizations

### Use a different translation API
Edit `backend/main.py`, function `translate_with_deepl()` or add a new function

### Change the UI colors
Edit `frontend/src/App.css`, look for `#667eea` (purple) color codes

### Add more languages
Modify the translation functions in `backend/main.py` to accept language parameters

---

Questions? Check the main README.md or the docstrings in the code!
