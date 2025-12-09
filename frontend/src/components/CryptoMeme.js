import React from 'react';
import { FaLaugh } from 'react-icons/fa';
import FeedbackButtons from './FeedbackButtons';

const CryptoMeme = ({ meme }) => {
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

  return (
    <div className="dashboard-card">
      <h2><FaLaugh /> Fun Crypto Meme</h2>
      <div className="meme-container">
        {meme.title && <h3 className="meme-title">{meme.title}</h3>}
        <img
          src={meme.url}
          alt={meme.title || 'Crypto meme'}
          className="meme-image"
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'block';
          }}
        />
        <div style={{ display: 'none', color: '#999', padding: '20px' }}>
          Image failed to load
        </div>
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

