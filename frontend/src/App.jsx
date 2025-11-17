import React, { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('search'); // 'search' or 'paste'
  const [artist, setArtist] = useState('');
  const [title, setTitle] = useState('');
  const [manualSpanish, setManualSpanish] = useState('');
  
  const [spanishLyrics, setSpanishLyrics] = useState('');
  const [englishLyrics, setEnglishLyrics] = useState('');
  const [wordPairs, setWordPairs] = useState([]); // line-by-line pairs
  const [wordTranslations, setWordTranslations] = useState([]); // word-by-word translations
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
        body: JSON.stringify({ artist, title }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch song');
      }

      const data = await response.json();
      setSpanishLyrics(data.spanish_lyrics);
      setEnglishLyrics(data.english_lyrics);
      setWordPairs(data.word_pairs);
      setWordTranslations(data.word_translations);
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
        body: JSON.stringify({ spanish_text: manualSpanish }),
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      setSpanishLyrics(data.spanish_lyrics);
      setEnglishLyrics(data.english_lyrics);
      setWordPairs(data.word_pairs);
      setWordTranslations(data.word_translations);
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
    setWordPairs([]);
    setWordTranslations([]);
    setAudioUrl(null);
    setError('');
  };

  // Helper function to create word spans with translations
  const createWordSpans = (line, lineIndex) => {
    if (!line.trim()) return <span className="empty-line">&nbsp;</span>;
    
    const words = line.split(/(\s+)/); // Split on whitespace but keep spaces
    const lineTranslations = wordTranslations.filter(wt => wt.line_index === lineIndex);
    
    return words.map((word, idx) => {
      if (!word.trim()) return word; // Return whitespace as-is
      
      const lowerWord = word.toLowerCase().replace(/[^\w]/g, '');
      const translation = lineTranslations.find(
        wt => wt.word === lowerWord
      );
      
      if (translation) {
        return (
          <span key={idx} className="word-with-translation" title={translation.translation}>
            {word}
          </span>
        );
      }
      return word;
    });
  };

  // Split into lines for display
  const spanishLines = spanishLyrics.split('\n');
  const englishLines = englishLyrics.split('\n');

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎵 Music Translator</h1>
        <p className="subtitle">Translate Spanish lyrics to English</p>
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
                <label>Paste Spanish Lyrics</label>
                <textarea
                  value={manualSpanish}
                  onChange={(e) => setManualSpanish(e.target.value)}
                  placeholder="Paste your Spanish lyrics here..."
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
                <h3>Spanish</h3>
                <div className="lyrics-content">
                  {spanishLines.map((line, idx) => (
                    <div key={idx} className="lyrics-line">
                      {createWordSpans(line, idx)}
                    </div>
                  ))}
                </div>
              </div>

              <div className="lyrics-column">
                <h3>English</h3>
                <div className="lyrics-content">
                  {englishLines.map((line, idx) => (
                    <div key={idx} className="lyrics-line">
                      {createWordSpans(line, idx)}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Line-by-Line Alignment */}
            {wordPairs.length > 0 && (
              <div className="word-alignment">
                <h3>📖 Line-by-Line Translation</h3>
                <div className="line-pairs-container">
                  {wordPairs.map((pair, idx) => (
                    <div key={idx} className="line-pair">
                      <div className="line-pair-spanish">
                        <strong>Spanish:</strong>
                        <p>{pair.spanish}</p>
                      </div>
                      <div className="line-pair-english">
                        <strong>English:</strong>
                        <p>{pair.english}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

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