#!/bin/bash

echo ""
echo "========================================"
echo "Music Translator - Setup"
echo "========================================"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "[ERROR] backend/.env file not found!"
    echo ""
    echo "Please do this first:"
    echo "1. Go to backend folder"
    echo "2. Copy .env.example to .env"
    echo "3. Edit .env and add your API keys:"
    echo "   - GENIUS_API_TOKEN"
    echo "   - DEEPL_API_KEY"
    echo "   - (optional) SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET"
    echo ""
    exit 1
fi

echo "[1/4] Creating Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "[2/4] Installing Python dependencies..."
pip install -r requirements.txt

echo "[3/4] Starting backend server..."
echo "Backend running on http://localhost:8000"
echo "[Keep this terminal open!]"
echo ""
python main.py &
BACKEND_PID=$!

sleep 3

echo "[4/4] Starting frontend..."
cd ../frontend
npm install
npm start

# Cleanup
trap "kill $BACKEND_PID" EXIT
