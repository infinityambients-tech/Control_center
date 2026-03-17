import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { registrationService } from '../../services/registrationService';
import '../../styles/EmailVerification.css';

interface EmailVerificationPage {
  onSuccess?: () => void;
}

type VerificationState = 'loading' | 'success' | 'error' | 'idle';

export const EmailVerification: React.FC<EmailVerificationPage> = ({ onSuccess }) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [state, setState] = useState<VerificationState>('idle');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState<string>('');

  useEffect(() => {
    const verifyEmail = async () => {
      const token = searchParams.get('token');

      if (!token) {
        setState('error');
        setMessage('No verification token provided. Please check the link in your email.');
        return;
      }

      setState('loading');

      try {
        const response = await registrationService.verifyEmail(token);

        if (response.success) {
          setState('success');
          setMessage(response.message);
          setStatus(response.status || '');

          if (onSuccess) {
            setTimeout(onSuccess, 3000);
          } else {
            // Redirect to login after 3 seconds
            setTimeout(() => {
              navigate('/login');
            }, 3000);
          }
        } else {
          setState('error');
          setMessage('Email verification failed. Please try again or request a new verification email.');
        }
      } catch (error: any) {
        setState('error');
        setMessage(error.message || 'An error occurred during verification. Please try again.');
        console.error('Verification error:', error);
      }
    };

    verifyEmail();
  }, [searchParams, navigate, onSuccess]);

  return (
    <div className="email-verification-container">
      <div className="verification-card">
        {state === 'loading' && (
          <>
            <Loader className="loading-icon" size={64} />
            <h1>Verifying Email...</h1>
            <p>Please wait while we verify your email address.</p>
          </>
        )}

        {state === 'success' && (
          <>
            <CheckCircle className="success-icon" size={64} color="#28a745" />
            <h1>Email Verified Successfully!</h1>
            <p>{message}</p>
            
            {status === 'active' && (
              <div className="status-box success-status">
                <strong>Your account is now active!</strong>
                <p>You can now log in and start using Control Center.</p>
              </div>
            )}

            {status === 'pending_company' && (
              <div className="status-box pending-status">
                <strong>Company account pending verification</strong>
                <p>Your email has been verified. Our team will now review your company information and send you a confirmation email once the verification is complete. This typically takes 1-2 business days.</p>
              </div>
            )}

            <p className="redirect-message">Redirecting to login page in 3 seconds...</p>
          </>
        )}

        {state === 'error' && (
          <>
            <AlertCircle className="error-icon" size={64} color="#dc3545" />
            <h1>Verification Failed</h1>
            <p>{message}</p>

            <div className="error-actions">
              <button className="action-btn primary" onClick={() => navigate('/login')}>
                Go to Login
              </button>
              <button
                className="action-btn secondary"
                onClick={() => navigate('/register')}
              >
                Register Again
              </button>
            </div>

            <p className="help-text">
              If you continue to have issues, please contact our support team at support@control-center.pl
            </p>
          </>
        )}

        {state === 'idle' && <div></div>}
      </div>
    </div>
  );
};

export const EmailVerificationSuccess: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  React.useEffect(() => {
    // After redirect, server may have set HttpOnly auth cookies; verify session by calling /auth/me
    let mounted = true;
    (async () => {
      try {
        const resp = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/auth/me`, { credentials: 'include' });
        if (!mounted) return;
        if (resp.ok) {
          // authenticated, go to app
          setTimeout(() => { navigate('/', { replace: true }); try { window.location.reload(); } catch (e) {} }, 800);
        }
      } catch (e) {
        // ignore
      }
    })();
    return () => { mounted = false; };
  }, [searchParams, navigate]);

  const email = searchParams.get('email');

  return (
    <div className="email-verification-container">
      <div className="verification-card">
        <CheckCircle className="success-icon" size={64} color="#28a745" />
        <h1>Email Verified!</h1>
        <p>Your email address has been successfully verified.</p>
        {email && <p>Logged in as <strong>{email}</strong> (if auto-login was enabled)</p>}
        <p>Click below to log in to your account.</p>

        <button className="action-btn primary" onClick={() => navigate('/login')}> 
          Go to Login
        </button>
      </div>
    </div>
  );
};

export const EmailVerificationError: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="email-verification-container">
      <div className="verification-card">
        <AlertCircle className="error-icon" size={64} color="#dc3545" />
        <h1>Verification Error</h1>
        <p>The verification link is invalid or has expired.</p>
        <p>Please request a new verification email or contact support.</p>

        <div className="error-actions">
          <button className="action-btn primary" onClick={() => navigate('/register')}>
            Request New Verification
          </button>
          <button className="action-btn secondary" onClick={() => navigate('/login')}>
            Go to Login
          </button>
        </div>
      </div>
    </div>
  );
};
