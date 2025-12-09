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
        {dashboardData?.news && dashboardData.news.length > 0 && (
          <MarketNews news={dashboardData.news} />
        )}
        
        {dashboardData?.prices && dashboardData.prices.length > 0 && (
          <CoinPrices prices={dashboardData.prices} />
        )}
        
        {dashboardData?.ai_insight && dashboardData.ai_insight.text && (
          <AIInsight insight={dashboardData.ai_insight} />
        )}
        
        {dashboardData?.meme && dashboardData.meme.url && (
          <CryptoMeme meme={dashboardData.meme} />
        )}
      </div>

      {(!dashboardData || 
        (!dashboardData.news?.length && 
         !dashboardData.prices?.length && 
         !dashboardData.ai_insight?.text && 
         !dashboardData.meme?.url)) && (
        <div className="dashboard-card">
          <p>No content available. Please check your preferences or try refreshing.</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

