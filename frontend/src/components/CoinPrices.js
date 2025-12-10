import React from 'react';
import { FaCoins } from 'react-icons/fa';
import FeedbackButtons from './FeedbackButtons';

const CoinPrices = ({ prices }) => {
  if (!prices || prices.length === 0) {
    return (
      <div className="dashboard-card">
        <h2><FaCoins /> Coin Prices</h2>
        <div className="card-content">
          <p>No price data available at the moment.</p>
        </div>
      </div>
    );
  }

  const formatPrice = (price) => {
    if (price >= 1) {
      return `$${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    } else {
      return `$${price.toFixed(6)}`;
    }
  };

  const formatChange = (change) => {
    if (change === null || change === undefined) return '';
    const sign = change >= 0 ? '+' : '';
    return `${sign}${change.toFixed(2)}%`;
  };

  return (
    <div className="dashboard-card">
      <h2><FaCoins /> Coin Prices</h2>
      <div className="coin-list">
        {prices.map((coin, index) => (
          <div key={coin.id || index} className="coin-item">
            <div className="coin-info">
              <span className="coin-name">
                {coin.name}
                {coin.symbol && <span className="coin-symbol">({coin.symbol})</span>}
              </span>
              {coin.content_hash && (
                <FeedbackButtons
                  contentType="price"
                  contentHash={coin.content_hash}
                />
              )}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', flexShrink: 0 }}>
              <span className="coin-price">{formatPrice(coin.price_usd)}</span>
              {coin.price_change_24h !== undefined && (
                <span className={`coin-change ${coin.price_change_24h >= 0 ? 'positive' : 'negative'}`}>
                  {formatChange(coin.price_change_24h)}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CoinPrices;

