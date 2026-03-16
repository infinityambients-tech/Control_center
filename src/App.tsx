import React, { useState, useEffect } from 'react';
import { HashRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Portfolio } from './modules/portfolio/Portfolio';
import Finance from './modules/finance/Finance';
import Subscriptions from './modules/subscriptions/Subscriptions';
import Roadmap from './modules/roadmap/Roadmap';
import Deployments from './modules/deployments/Deployments';
import Settings from './modules/settings/Settings';
import Updates from './modules/updates/Updates';
import { Login } from './modules/auth/Login';
import { Register } from './modules/auth/Register';
import { EmailVerification, EmailVerificationSuccess, EmailVerificationError } from './modules/auth/EmailVerification';
import { Audit } from './modules/audit/Audit';
import Plans from './modules/plans/Plans';
import { authService } from './services/authService';
import { realtimeService } from './services/realtimeService';

function ProtectedRoute({ element, isAuthenticated }: { element: React.ReactNode; isAuthenticated: boolean | null }) {
  if (isAuthenticated === null) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'white' }}>Loading...</div>;
  }
  return isAuthenticated ? element : <Navigate to="/login" replace />;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  const handleLogin = () => setIsAuthenticated(true);

  // Wrapper to provide navigation callback to Register component
  const RegisterWrapper: React.FC = () => {
    const nav = useNavigate();
    return <Register onSuccess={() => nav('/login')} />;
  };

  // Check session on app start (cookie-based auth)
  useEffect(() => {
    let mounted = true;
    authService.whoami().then(r => {
      if (!mounted) return;
      setIsAuthenticated(r.authenticated);
    }).catch(() => {
      if (mounted) setIsAuthenticated(false);
    });
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    // When authenticated, connect realtime WS (browser will send cookies for same-origin)
    if (isAuthenticated) {
      realtimeService.connect();

      // listen for company verification events
      const handler = (data: any) => {
        const payload = data.payload || data;
        if (payload && payload.status) {
          // Show a simple toast notification
          showToast(`Account status changed: ${payload.status}`);
          if (payload.status === 'active') {
            setTimeout(() => { try { window.location.reload(); } catch (e) { } }, 800);
          }
        }
      };
      realtimeService.on('company_verification', handler);

      return () => {
        realtimeService.off('company_verification', handler);
        realtimeService.disconnect();
      };
    } else {
      realtimeService.disconnect();
    }
  }, [isAuthenticated]);

  // lightweight toast helper
  function showToast(message: string) {
    const el = document.createElement('div');
    el.textContent = message;
    el.style.position = 'fixed';
    el.style.right = '20px';
    el.style.top = '20px';
    el.style.background = 'rgba(0,0,0,0.8)';
    el.style.color = 'white';
    el.style.padding = '10px 14px';
    el.style.borderRadius = '8px';
    el.style.zIndex = '9999';
    document.body.appendChild(el);
    setTimeout(() => { el.style.transition = 'opacity 0.3s'; el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 4000);
  }

  return (
    <Router>
      <Routes>
        {/* Auth Routes */}
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<RegisterWrapper />} />
        <Route path="/verify-email" element={<EmailVerification />} />
        <Route path="/verify-email-success" element={<EmailVerificationSuccess />} />
        <Route path="/verify-email-error" element={<EmailVerificationError />} />

        {/* Protected Routes */}
        <Route path="/" element={<ProtectedRoute element={<Portfolio />} isAuthenticated={isAuthenticated} />} />
        <Route path="/finance" element={<ProtectedRoute element={<Finance />} isAuthenticated={isAuthenticated} />} />
        <Route path="/subscriptions" element={<ProtectedRoute element={<Subscriptions />} isAuthenticated={isAuthenticated} />} />
        <Route path="/roadmap" element={<ProtectedRoute element={<Roadmap />} isAuthenticated={isAuthenticated} />} />
        <Route path="/deployments" element={<ProtectedRoute element={<Deployments />} isAuthenticated={isAuthenticated} />} />
        <Route path="/plans" element={<ProtectedRoute element={<Plans />} isAuthenticated={isAuthenticated} />} />
        <Route path="/audit" element={<ProtectedRoute element={<Audit />} isAuthenticated={isAuthenticated} />} />
        <Route path="/updates" element={<ProtectedRoute element={<Updates />} isAuthenticated={isAuthenticated} />} />
        <Route path="/settings" element={<ProtectedRoute element={<Settings />} isAuthenticated={isAuthenticated} />} />

        {/* Catch all - redirect to login if not authenticated, else to home */}
        <Route path="*" element={isAuthenticated === null ? <div /> : isAuthenticated ? <Navigate to="/" replace /> : <Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
