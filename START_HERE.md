# 📁 Your Music Translation Project Files

All your project files are here! Here's what you have:

## 📖 Read These First

1. **QUICKSTART.md** - 10 minute setup guide (start here!)
2. **README.md** - Full documentation and reference

## 🚀 Quick Setup (Choose Your OS)

### Windows Users
1. Read **QUICKSTART.md** first (5 min read)
2. Get your API keys (Genius, DeepL, Spotify - optional)
3. Go to `backend` folder
4. Copy `.env.example` to `.env`
5. Edit `.env` and paste your API keys
6. Double-click **START_APP_WINDOWS.bat**
7. App opens automatically in browser!

### Mac/Linux Users
1. Read **QUICKSTART.md** first (5 min read)
2. Get your API keys
3. Go to `backend` folder
4. Copy `.env.example` to `.env`
5. Edit `.env` and paste your API keys
6. Run: `bash START_APP.sh`
7. App opens in browser!

## 📂 Project Structure

```
your-project/
├── backend/
│   ├── main.py              ← Backend server code
│   ├── requirements.txt      ← Python dependencies
│   ├── .env.example          ← Copy to .env and add your keys
│   └── .env                  ← Your API keys (create this!)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           ← Main React component
│   │   ├── App.css           ← Styling
│   │   └── ...
│   ├── package.json
│   └── public/
│       └── index.html
│
├── QUICKSTART.md             ← Read this first!
├── README.md                 ← Full docs
├── START_APP_WINDOWS.bat     ← Run this (Windows)
└── START_APP.sh              ← Run this (Mac/Linux)
```

## 🔑 Get Your API Keys (5 minutes)

### 1️⃣ Genius API (Required)
- Go to: https://genius.com/api-clients
- Click "Generate Access Token"
- Copy the token
- Paste in `.env` as: `GENIUS_API_TOKEN=your_token_here`

### 2️⃣ DeepL API (Recommended, Free)
- Go to: https://www.deepl.com/pro-api
- Click "Start for free"
- Copy your API Key
- Paste in `.env` as: `DEEPL_API_KEY=your_key_here`

### 3️⃣ Spotify (Optional, for audio preview)
- Go to: https://developer.spotify.com/dashboard
- Create an App
- Copy Client ID and Secret
- Paste in `.env` as:
  ```
  SPOTIFY_CLIENT_ID=your_id_here
  SPOTIFY_CLIENT_SECRET=your_secret_here
  ```

## ⚙️ Manual Setup (If Scripts Don't Work)

### Backend
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

### Frontend (Open NEW terminal)
```bash
cd frontend
npm install
npm start
```

## 🎯 How to Use

Once running:
1. Go to http://localhost:3000 in your browser
2. Enter song artist name (e.g., "Gente de Zona")
3. Enter song title (e.g., "Dale la Vuelta")
4. Click "Search & Translate"
5. See Spanish lyrics on left, English on right!

Or use "Paste Lyrics" tab to manually paste Spanish lyrics.

## ❓ Troubleshooting

### "Module not found" or "pip command not found"
- Make sure Python is installed: `python --version`
- On Mac, might need: `python3 -m venv venv`

### Backend won't start
- Check `.env` file exists and has your API keys
- Make sure port 8000 is not in use
- Try: `python -m pip install -r requirements.txt`

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Try: `npm cache clean --force` then `npm install`
- Delete `node_modules` folder and try again

### "No lyrics found"
- Try a different spelling
- Check the song exists on https://genius.com

### Translation errors
- Check your DeepL API key is correct and has quota
- App will fall back to free MyMemory API if DeepL fails

## 📞 Need Help?

1. Check **QUICKSTART.md** for detailed setup
2. Check **README.md** for full documentation
3. Check the code comments (well documented!)
4. Test each API key individually on their websites

## ✨ Next Steps After Getting It Working

1. Search for your favorite Spanish songs!
2. Try the "Paste Lyrics" mode
3. Check out word-by-word translations
4. Listen to audio previews

Then explore:
- Customizing colors in `frontend/src/App.css`
- Adding new features in `backend/main.py`
- Deploying to the web (see README.md)

---

Happy translating! 🎵
