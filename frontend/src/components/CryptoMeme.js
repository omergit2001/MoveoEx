import React, { useState } from 'react';
import { FaLaugh } from 'react-icons/fa';
import FeedbackButtons from './FeedbackButtons';

const CryptoMeme = ({ meme }) => {
  const [imageError, setImageError] = useState(false);
  
  if (!meme || !meme.url) {
    return (
      <div className="dashboard-card">
        <h2><FaLaugh /> Fun Crypto Meme</h2>
        <div className="card-content">
          <p>No meme available at the moment.</p>
        </div>
      </div>
    );
  }

  // Generate a simple SVG placeholder as fallback
  const generatePlaceholder = (title) => {
    const svg = `<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="400" fill="#667eea"/><text x="50%" y="50%" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">${title || 'Crypto Meme'}</text></svg>`;
    return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  };

  const handleImageError = (e) => {
    setImageError(true);
    // Try to use SVG placeholder as fallback
    e.target.src = generatePlaceholder(meme.title);
    e.target.onerror = null; // Prevent infinite loop
  };

  return (
    <div className="dashboard-card">
      <h2><FaLaugh /> Fun Crypto Meme</h2>
      <div className="meme-container">
        {meme.title && <h3 className="meme-title">{meme.title}</h3>}
        <img
          src={meme.url}
          alt={meme.title || 'Crypto meme'}
          className="meme-image"
          onError={handleImageError}
        />
        {meme.description && (
          <p style={{ color: '#666', fontSize: '14px', marginTop: '10px' }}>
            {meme.description}
          </p>
        )}
        {meme.content_hash && (
          <FeedbackButtons
            contentType="meme"
            contentHash={meme.content_hash}
          />
        )}
      </div>
    </div>
  );
};

export default CryptoMeme;

