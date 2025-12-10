import React, { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/auth';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const errorRef = useRef('');
  const navigate = useNavigate();

  // Keep error state in sync with ref - restore if it gets cleared accidentally
  useEffect(() => {
    if (errorRef.current && !error) {
      setError(errorRef.current);
    }
  }, [error]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    errorRef.current = '';
    setError('');
    setLoading(true);

    try {
      const response = await authService.login(email, password);
      
      // Check if user has preferences
      if (response.user && !response.user.has_preferences) {
        navigate('/onboarding');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      const errorMessage = err.error || 'Login failed. Please check your credentials.';
      errorRef.current = errorMessage;
      setError(errorMessage);
      // Clear fields on error but keep error message displayed
      setEmail('');
      setPassword('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>Login</h1>
        <form onSubmit={handleSubmit} className="auth-form">
          {(error || errorRef.current) && (
            <div key="error-message" className="error-message">
              {error || errorRef.current}
            </div>
          )}
          
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                // Restore error if it exists and user is typing
                if (errorRef.current && !error) {
                  setError(errorRef.current);
                }
              }}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                // Restore error if it exists and user is typing
                if (errorRef.current && !error) {
                  setError(errorRef.current);
                }
              }}
              required
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="text-center mt-20">
          <p>Don't have an account? <Link to="/signup" className="link">Sign up</Link></p>
        </div>
      </div>
    </div>
  );
};

export default Login;

