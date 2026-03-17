import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { authService } from '../../services/authService';
import { Mail, Lock, Boxes } from 'lucide-react';

interface LoginProps {
  onLogin: () => void;
}

export const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const prefill = searchParams.get('email');
    if (prefill) {
      setEmail(prefill);
    } else {
      const savedEmail = localStorage.getItem('rememberedEmail');
      const savedPassword = localStorage.getItem('rememberedPassword');
      if (savedEmail) setEmail(savedEmail);
      if (savedPassword) {
        setPassword(savedPassword);
        setRememberMe(true);
      }
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await authService.login(email, password);
    if (result.success) {
      if (rememberMe) {
        localStorage.setItem('rememberedEmail', email);
        localStorage.setItem('rememberedPassword', password);
      } else {
        localStorage.removeItem('rememberedEmail');
        localStorage.removeItem('rememberedPassword');
      }

      // Force a check to load session
      await authService.whoami();
      onLogin();
      navigate('/');
    } else {
      // Show backend-provided message when available (e.g., Email not verified)
      setError(result.message || 'Invalid credentials. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-card fade-in">
        <div className="login-header">
          <Boxes size={48} color="#0070f3" />
          <h1>Control Center</h1>
          <p>Login to your central dashboard</p>
        </div>

        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label><Mail size={16} /> Email</label>
            <input
              required
              type="email"
              placeholder="admin@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label><Lock size={16} /> Password</label>
            <input
              required
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>

          <div className="form-group" style={{ flexDirection: 'row', alignItems: 'center', gap: '8px' }}>
            <input
              type="checkbox"
              id="rememberMe"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              style={{ width: '16px', height: '16px', accentColor: '#0070f3', cursor: 'pointer' }}
            />
            <label htmlFor="rememberMe" style={{ cursor: 'pointer', margin: 0 }}>Zapamiętaj mnie (Mail i Hasło)</label>
          </div>

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="login-footer">
          <p>Phase 2: Centralized Architecture</p>
          <div className="signup-section">
            <p>Don't have an account?</p>
            <button
              type="button"
              className="signup-btn"
              onClick={() => navigate('/register')}
            >
              Create Account
            </button>
          </div>
        </div>
      </div>

      <style>{`
        .login-container {
          width: 100vw;
          height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: var(--bg-dark);
        }

        .login-card {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: 24px;
          padding: 48px;
          width: 400px;
          display: flex;
          flex-direction: column;
          gap: 32px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .login-header {
          text-align: center;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 12px;
        }

        .login-header h1 {
          font-size: 1.8rem;
          font-weight: 800;
          letter-spacing: -0.03em;
        }

        .login-header p {
          color: var(--text-secondary);
          font-size: 0.95rem;
        }

        .form-group {
          margin-bottom: 20px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-group label {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.9rem;
          color: var(--text-secondary);
        }

        input {
          background: var(--bg-dark);
          border: 1px solid var(--border);
          border-radius: 10px;
          padding: 14px;
          color: var(--text-primary);
          font-size: 1rem;
        }

        input:focus {
          outline: none;
          border-color: var(--accent);
        }

        .login-btn {
          width: 100%;
          background: var(--accent);
          color: white;
          border: none;
          padding: 14px;
          border-radius: 10px;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: transform 0.2s;
          margin-top: 12px;
        }

        .login-btn:hover {
          transform: translateY(-2px);
        }

        .error-message {
          background: rgba(255, 68, 68, 0.1);
          color: #ff4444;
          padding: 12px;
          border-radius: 8px;
          font-size: 0.85rem;
          text-align: center;
        }

        .login-footer {
          text-align: center;
          font-size: 0.75rem;
          color: var(--text-secondary);
          opacity: 0.5;
        }

        .signup-section {
          margin-top: 20px;
          padding-top: 20px;
          border-top: 1px solid var(--border);
          opacity: 1;
        }

        .signup-section p {
          font-size: 0.9rem;
          margin-bottom: 12px;
          opacity: 1;
          color: var(--text-secondary);
        }

        .signup-btn {
          width: 100%;
          background: linear-gradient(135deg, var(--accent) 0%, #0057cc 100%);
          color: white;
          border: none;
          padding: 12px;
          border-radius: 10px;
          font-weight: 600;
          font-size: 0.95rem;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .signup-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 20px rgba(0, 112, 243, 0.4);
        }

        .signup-btn:active {
          transform: translateY(0);
        }
      `}</style>
    </div>
  );
};
