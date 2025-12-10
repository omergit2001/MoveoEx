import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaSync } from 'react-icons/fa';
import { authService } from '../services/auth';
import api from '../services/api';
import MarketNews from './MarketNews';
import CoinPrices from './CoinPrices';
import AIInsight from './AIInsight';
import CryptoMeme from './CryptoMeme';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [userPreferences, setUserPreferences] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check authentication
    if (!authService.isAuthenticated()) {
      navigate('/login');
      return;
    }

    // Get user info
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);

    // Fetch dashboard data
    fetchDashboard();
  }, [navigate]);

  const fetchDashboard = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await api.get('/dashboard');
      setDashboardData(response.data.dashboard);
      setUserPreferences(response.data.user_preferences);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load dashboard. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  const handleRefresh = () => {
    fetchDashboard();
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error && !dashboardData) {
    return (
      <div className="dashboard-container">
        <div className="dashboard-card">
          <div className="error-message">{error}</div>
          <button className="btn btn-primary" onClick={fetchDashboard} style={{ marginTop: '20px' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div>
          <h1>Welcome back{user?.name ? `, ${user.name}` : ''}!</h1>
          <p style={{ color: '#666', marginTop: '5px' }}>Your personalized crypto dashboard</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            className="btn btn-secondary"
            onClick={handleRefresh}
            title="Refresh dashboard"
          >
            <FaSync /> Refresh
          </button>
          <button
            className="btn btn-secondary"
            onClick={handleLogout}
            title="Logout"
          >
            <FaSignOutAlt /> Logout
          </button>
        </div>
      </div>

      {error && (
        <div className="dashboard-card" style={{ marginBottom: '20px', background: '#fff3cd', border: '1px solid #ffc107' }}>
          <div className="error-message">{error}</div>
        </div>
      )}

      <div className="dashboard-grid">
        {/* Display sections based on user's content type preferences */}
        {userPreferences?.content_types?.includes('Market News') && (
          <MarketNews news={dashboardData?.news || []} />
        )}
        {userPreferences?.content_types?.includes('Charts') && (
          <CoinPrices prices={dashboardData?.prices || []} />
        )}
        {userPreferences?.content_types?.includes('Social') && (
          <AIInsight insight={dashboardData?.ai_insight || {}} />
        )}
        {userPreferences?.content_types?.includes('Fun') && (
          <CryptoMeme meme={dashboardData?.meme || {}} />
        )}
      </div>
    </div>
  );
};

export default Dashboard;

