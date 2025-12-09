import React, { useState } from 'react';
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa';
import api from '../services/api';

const FeedbackButtons = ({ contentType, contentHash }) => {
  const [vote, setVote] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVote = async (voteValue) => {
    if (loading) return;
    
    setLoading(true);
    try {
      await api.post('/feedback', {
        content_type: contentType,
        content_hash: contentHash,
        vote: voteValue
      });
      setVote(voteValue);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="feedback-buttons">
      <button
        className={`feedback-btn ${vote === 1 ? 'active' : ''}`}
        onClick={() => handleVote(1)}
        disabled={loading}
        title="Thumbs up"
      >
        <FaThumbsUp /> Like
      </button>
      <button
        className={`feedback-btn ${vote === -1 ? 'active thumbs-down' : ''}`}
        onClick={() => handleVote(-1)}
        disabled={loading}
        title="Thumbs down"
      >
        <FaThumbsDown /> Dislike
      </button>
    </div>
  );
};

export default FeedbackButtons;

