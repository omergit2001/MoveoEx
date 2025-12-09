import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { authService } from '../services/auth';

const Onboarding = () => {
  const [step, setStep] = useState(1);
  const [interestedAssets, setInterestedAssets] = useState([]);
  const [investorType, setInvestorType] = useState('');
  const [contentTypes, setContentTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const availableAssets = [
    'Bitcoin', 'Ethereum', 'Binance Coin', 'Cardano', 'Solana',
    'Ripple', 'Polkadot', 'Dogecoin', 'Chainlink', 'Litecoin'
  ];

  const investorTypes = [
    'HODLer',
    'Day Trader',
    'NFT Collector',
    'DeFi Enthusiast',
    'General Investor'
  ];

  const availableContentTypes = [
    'Market News',
    'Charts',
    'Social',
    'Fun'
  ];

  const handleAssetToggle = (asset) => {
    setInterestedAssets(prev => 
      prev.includes(asset)
        ? prev.filter(a => a !== asset)
        : [...prev, asset]
    );
  };

  const handleContentTypeToggle = (type) => {
    setContentTypes(prev =>
      prev.includes(type)
        ? prev.filter(t => t !== type)
        : [...prev, type]
    );
  };

  const handleNext = () => {
    if (step === 1 && interestedAssets.length === 0) {
      setError('Please select at least one crypto asset.');
      return;
    }
    if (step === 2 && !investorType) {
      setError('Please select your investor type.');
      return;
    }
    if (step === 3 && contentTypes.length === 0) {
      setError('Please select at least one content type.');
      return;
    }
    setError('');
    if (step < 3) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      setError('');
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      await api.post('/user/preferences', {
        investor_type: investorType,
        interested_assets: interestedAssets,
        content_types: contentTypes
      });

      // Fetch updated user from API to get latest preferences status
      try {
        const updatedUser = await authService.getCurrentUserFromAPI();
        if (updatedUser) {
          localStorage.setItem('user', JSON.stringify(updatedUser));
        }
      } catch (apiError) {
        // If API call fails, update localStorage manually
        const userStr = localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          user.has_preferences = true;
          localStorage.setItem('user', JSON.stringify(user));
        }
      }

      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save preferences. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <h1>Welcome! Let's personalize your dashboard</h1>
        <p style={{ color: '#666', marginBottom: '30px' }}>
          Answer a few questions to get started
        </p>

        {error && <div className="error-message">{error}</div>}

        {/* Step 1: Crypto Assets */}
        {step === 1 && (
          <div className="onboarding-step">
            <h2>What crypto assets are you interested in?</h2>
            <p style={{ color: '#666', marginBottom: '15px' }}>
              Select one or more cryptocurrencies
            </p>
            <div className="checkbox-group">
              {availableAssets.map(asset => (
                <div
                  key={asset}
                  className={`checkbox-item ${interestedAssets.includes(asset) ? 'active' : ''}`}
                  onClick={() => handleAssetToggle(asset)}
                >
                  <input
                    type="checkbox"
                    checked={interestedAssets.includes(asset)}
                    readOnly
                    tabIndex={-1}
                  />
                  <label>{asset}</label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Investor Type */}
        {step === 2 && (
          <div className="onboarding-step">
            <h2>What type of investor are you?</h2>
            <p style={{ color: '#666', marginBottom: '15px' }}>
              Choose the option that best describes you
            </p>
            <div className="radio-group">
              {investorTypes.map(type => (
                <div
                  key={type}
                  className={`radio-item ${investorType === type ? 'active' : ''}`}
                  onClick={() => setInvestorType(type)}
                >
                  <input
                    type="radio"
                    name="investorType"
                    checked={investorType === type}
                    readOnly
                    tabIndex={-1}
                  />
                  <label>{type}</label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Content Types */}
        {step === 3 && (
          <div className="onboarding-step">
            <h2>What kind of content would you like to see?</h2>
            <p style={{ color: '#666', marginBottom: '15px' }}>
              Select one or more content types
            </p>
            <div className="checkbox-group">
              {availableContentTypes.map(type => (
                <div
                  key={type}
                  className={`checkbox-item ${contentTypes.includes(type) ? 'active' : ''}`}
                  onClick={() => handleContentTypeToggle(type)}
                >
                  <input
                    type="checkbox"
                    checked={contentTypes.includes(type)}
                    readOnly
                    tabIndex={-1}
                  />
                  <label>{type}</label>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="onboarding-navigation">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleBack}
            disabled={step === 1 || loading}
          >
            Back
          </button>
          <button
            type="button"
            className="btn btn-primary"
            onClick={handleNext}
            disabled={loading}
          >
            {loading ? 'Saving...' : step === 3 ? 'Complete' : 'Next'}
          </button>
        </div>

        {/* Progress indicator */}
        <div style={{ marginTop: '30px', textAlign: 'center' }}>
          <span style={{ color: '#999' }}>
            Step {step} of 3
          </span>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;

