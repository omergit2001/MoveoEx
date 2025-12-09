import React from 'react';
import { FaNewspaper } from 'react-icons/fa';
import FeedbackButtons from './FeedbackButtons';

const MarketNews = ({ news }) => {
  if (!news || news.length === 0) {
    return (
      <div className="dashboard-card">
        <h2><FaNewspaper /> Market News</h2>
        <div className="card-content">
          <p>No news available at the moment.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-card">
      <h2><FaNewspaper /> Market News</h2>
      <div className="news-list">
        {news.map((item, index) => (
          <div key={item.id || index} className="news-item">
            <h3>{item.title}</h3>
            {item.url && (
              <a href={item.url} target="_blank" rel="noopener noreferrer">
                Read more →
              </a>
            )}
            <div className="news-meta">
              {item.source && <span>Source: {item.source}</span>}
              {item.currencies && item.currencies.length > 0 && (
                <span style={{ marginLeft: '10px' }}>
                  {item.currencies.join(', ')}
                </span>
              )}
            </div>
            {item.content_hash && (
              <FeedbackButtons
                contentType="news"
                contentHash={item.content_hash}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MarketNews;

