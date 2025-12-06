import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('search'); // 'search' or 'paste'
  const [artist, setArtist] = useState('');
  const [title, setTitle] = useState('');
  const [manualSpanish, setManualSpanish] = useState('');
  const [sourceLanguage, setSourceLanguage] = useState('ES');
  const [targetLanguage, setTargetLanguage] = useState('EN-US');
  
  const [spanishLyrics, setSpanishLyrics] = useState('');
  const [englishLyrics, setEnglishLyrics] = useState('');
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Refs for synced scrolling
  const spanishColRef = useRef(null);
  const englishColRef = useRef(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Synced scrolling effect
  useEffect(() => {
    const spanishCol = spanishColRef.current;
    const englishCol = englishColRef.current;
    
    if (!spanishCol || !englishCol) return;
    
    const handleScroll = (source, target) => {
      target.scrollTop = source.scrollTop;
    };
    
    spanishCol.addEventListener('scroll', () => handleScroll(spanishCol, englishCol));
    englishCol.addEventListener('scroll', () => handleScroll(englishCol, spanishCol));
    
    return () => {
      spanishCol.removeEventListener('scroll', () => handleScroll(spanishCol, englishCol));
      englishCol.removeEventListener('scroll', () => handleScroll(englishCol, spanishCol));
    };
  }, [spanishLyrics, englishLyrics]);

  const handleSearchSong = async (e) => {
    e.preventDefault();
    
    if (!artist.trim() || !title.trim()) {
      setError('Please enter both artist and song title');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/translate-song`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artist, title, source_language: sourceLanguage, target_language: targetLanguage }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch song');
      }

      const data = await response.json();
      setSpanishLyrics(data.spanish_lyrics);
      setEnglishLyrics(data.english_lyrics);
      setAudioUrl(data.audio_url);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTranslateManual = async (e) => {
    e.preventDefault();

    if (!manualSpanish.trim()) {
      setError('Please paste some Spanish lyrics');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE_URL}/translate-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ spanish_text: manualSpanish, source_language: sourceLanguage, target_language: targetLanguage }),
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      setSpanishLyrics(data.spanish_lyrics);
      setEnglishLyrics(data.english_lyrics);
      setAudioUrl(null);
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const clearResults = () => {
    setSpanishLyrics('');
    setEnglishLyrics('');
    setAudioUrl(null);
    setError('');
  };

  // Split into lines for display
  const spanishLines = spanishLyrics.split('\n');
  const englishLines = englishLyrics.split('\n');

  const getLanguageName = (code) => {
    const languages = {
      'ES': 'Spanish',
      'EN-US': 'English',
      'EN': 'English',
      'PT-BR': 'Portuguese',
      'PT': 'Portuguese (PT)',
      'FR': 'French',
      'DE': 'German',
      'IT': 'Italian',
      'NL': 'Dutch',
      'PL': 'Polish',
      'RU': 'Russian',
      'JA': 'Japanese',
      'ZH': 'Chinese',
      'KO': 'Korean',
      'TR': 'Turkish',
    };
    return languages[code] || 'another language';
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎵 Music Translator</h1>
        <p className="subtitle">Translate {getLanguageName(sourceLanguage)} to {getLanguageName(targetLanguage)}</p>
      </header>

      <div className="container">
        {/* Input Section */}
        <div className="input-section">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'search' ? 'active' : ''}`}
              onClick={() => setActiveTab('search')}
            >
              Search Song
            </button>
            <button
              className={`tab ${activeTab === 'paste' ? 'active' : ''}`}
              onClick={() => setActiveTab('paste')}
            >
              Paste Lyrics
            </button>
          </div>

          {/* Language Selection */}
          <div className="language-selectors">
            <div className="language-selector">
              <label htmlFor="source-lang">From:</label>
              <select 
                id="source-lang"
                value={sourceLanguage} 
                onChange={(e) => setSourceLanguage(e.target.value)}
                disabled={loading}
              >
                <option value="ES">Spanish</option>
                <option value="EN-US">English (US)</option>
                <option value="PT-BR">Portuguese (Brazil)</option>
                <option value="PT">Portuguese (Portugal)</option>
                <option value="FR">French</option>
                <option value="DE">German</option>
                <option value="IT">Italian</option>
                <option value="NL">Dutch</option>
                <option value="PL">Polish</option>
                <option value="RU">Russian</option>
                <option value="JA">Japanese</option>
                <option value="ZH">Chinese</option>
                <option value="KO">Korean</option>
                <option value="TR">Turkish</option>
              </select>
            </div>

            <div className="language-selector">
              <label htmlFor="target-lang">To:</label>
              <select 
                id="target-lang"
                value={targetLanguage} 
                onChange={(e) => setTargetLanguage(e.target.value)}
                disabled={loading}
              >
                <option value="EN-US">English (US)</option>
                <option value="ES">Spanish</option>
                <option value="PT-BR">Portuguese (Brazil)</option>
                <option value="PT">Portuguese (Portugal)</option>
                <option value="FR">French</option>
                <option value="DE">German</option>
                <option value="IT">Italian</option>
                <option value="NL">Dutch</option>
                <option value="PL">Polish</option>
                <option value="RU">Russian</option>
                <option value="JA">Japanese</option>
                <option value="ZH">Chinese</option>
                <option value="KO">Korean</option>
                <option value="TR">Turkish</option>
              </select>
            </div>
          </div>

          {activeTab === 'search' && (
            <form onSubmit={handleSearchSong} className="search-form">
              <div className="form-group">
                <label>Artist Name</label>
                <input
                  type="text"
                  value={artist}
                  onChange={(e) => setArtist(e.target.value)}
                  placeholder="e.g., Juanes"
                  disabled={loading}
                />
              </div>
              <div className="form-group">
                <label>Song Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., La Camisa Negra"
                  disabled={loading}
                />
              </div>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Searching...' : 'Search & Translate'}
              </button>
            </form>
          )}

          {activeTab === 'paste' && (
            <form onSubmit={handleTranslateManual} className="paste-form">
              <div className="form-group">
                <label>Paste {getLanguageName(sourceLanguage)} Lyrics</label>
                <textarea
                  value={manualSpanish}
                  onChange={(e) => setManualSpanish(e.target.value)}
                  placeholder={`Paste your ${getLanguageName(sourceLanguage).toLowerCase()} lyrics here...`}
                  rows="8"
                  disabled={loading}
                />
              </div>
              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Translating...' : 'Translate'}
              </button>
            </form>
          )}

          {error && <div className="error-message">{error}</div>}
        </div>

        {/* Results Section */}
        {spanishLyrics && (
          <div className="results-section">
            {audioUrl && (
              <div className="audio-player">
                <h3>🎧 Preview</h3>
                <audio controls src={audioUrl} />
              </div>
            )}

            {/* Lyrics Comparison */}
            <div className="lyrics-comparison">
              <div className="lyrics-column">
                <h3>{getLanguageName(sourceLanguage)}</h3>
                <div className="lyrics-content" ref={spanishColRef}>
                  {spanishLines.map((line, idx) => (
                    <div key={idx} className="lyrics-line">
                      {line || <span className="empty-line">&nbsp;</span>}
                    </div>
                  ))}
                </div>
              </div>

              <div className="lyrics-column">
                <h3>{getLanguageName(targetLanguage)}</h3>
                <div className="lyrics-content" ref={englishColRef}>
                  {englishLines.map((line, idx) => (
                    <div key={idx} className="lyrics-line">
                      {line || <span className="empty-line">&nbsp;</span>}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <button onClick={clearResults} className="btn-clear">
              Clear Results
            </button>
          </div>
        )}

        {!spanishLyrics && !loading && (
          <div className="empty-state">
            <p>👉 Search for a song or paste lyrics to get started</p>
          </div>
        )}
      </div>

      <footer className="app-footer">
        <p>💡 Powered by Genius, DeepL & Spotify APIs</p>
      </footer>
    </div>
  );
}

export default App;