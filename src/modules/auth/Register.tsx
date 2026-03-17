import React, { useState } from 'react';
import { AlertCircle, CheckCircle, User, Building2, Eye, EyeOff } from 'lucide-react';
import { registrationService } from '../../services/registrationService';
import '../../styles/Register.css';

interface RegistrationFormData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  password_confirm: string;
  phone: string;
  street: string;
  postal_code: string;
  city: string;
  country: string;
  is_company: boolean;
  company_details?: {
    company_name: string;
    nip: string;
    regon: string;
    krs: string;
    company_address: string;
    company_postal_code: string;
    company_city: string;
    company_country: string;
    contact_person: string;
    company_phone: string;
    company_email: string;
  };
  accept_terms: boolean;
  accept_gdpr: boolean;
}

interface FormErrors {
  [key: string]: string;
}

export const Register: React.FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
  const [step, setStep] = useState<'account-type' | 'form' | 'success'>('account-type');
  const [formData, setFormData] = useState<RegistrationFormData>({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    password_confirm: '',
    phone: '',
    street: '',
    postal_code: '',
    city: '',
    country: 'PL',
    is_company: false,
    company_details: {
      company_name: '',
      nip: '',
      regon: '',
      krs: '',
      company_address: '',
      company_postal_code: '',
      company_city: '',
      company_country: 'PL',
      contact_person: '',
      company_phone: '',
      company_email: '',
    },
    accept_terms: false,
    accept_gdpr: false,
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);
  const [generalError, setGeneralError] = useState('');
  const [emailAvailabilityStatus, setEmailAvailabilityStatus] = useState<'idle' | 'checking' | 'available' | 'taken'>('idle');
  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] = useState(false);
  const [successEmail, setSuccessEmail] = useState('');
  const [passwordStrength, setPasswordStrength] = useState(0);

  const handleAccountTypeSelect = (isCompany: boolean) => {
    setFormData({ ...formData, is_company: isCompany });
    setStep('form');
    setErrors({});
    setGeneralError('');
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>, section: 'personal' | 'company' = 'personal') => {
    const { name, value, type } = e.currentTarget;
    const checked = (e.currentTarget as HTMLInputElement).checked;

    if (section === 'company' && formData.company_details) {
      setFormData({
        ...formData,
        company_details: {
          ...formData.company_details,
          [name]: type === 'checkbox' ? checked : value,
        },
      });
    } else {
      setFormData({
        ...formData,
        [name]: type === 'checkbox' ? checked : value,
      });
    }

    // Update password strength indicator
    if (name === 'password') {
      setPasswordStrength(registrationService.getPasswordStrength(value));
    }

    // Clear field error when user starts typing
    if (errors[name]) {
      const newErrors = { ...errors };
      delete newErrors[name];
      setErrors(newErrors);
    }
  };

  const handleEmailChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const email = e.currentTarget.value;
    setFormData({ ...formData, email });

    // Clear email-specific errors
    const newErrors = { ...errors };
    delete newErrors.email;
    setErrors(newErrors);

    if (email.length === 0) {
      setEmailAvailabilityStatus('idle');
      return;
    }

    // Debounce email check (simplified - in production use useCallback + debounce hook)
    setEmailAvailabilityStatus('checking');
    try {
      const result = await registrationService.checkEmailAvailability(email);
      if (result.available) {
        setEmailAvailabilityStatus('available');
      } else {
        setEmailAvailabilityStatus('taken');
        setErrors({ ...newErrors, email: 'Email already registered' });
      }
    } catch {
      setEmailAvailabilityStatus('idle');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setGeneralError('');
    setErrors({});

    // Validate form
    const formErrors = registrationService.validateForm(formData);
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      setLoading(false);
      return;
    }

    // Check email availability once more
    if (emailAvailabilityStatus !== 'available') {
      setErrors({ email: 'Email not available' });
      setLoading(false);
      return;
    }

    try {
      const response = await registrationService.register(formData);
      if (response.success) {
        setSuccessEmail(formData.email);
        setStep('success');
        if (onSuccess) {
          setTimeout(onSuccess, 3000);
        }
      }
    } catch (error: any) {
      const errorMsg = error.message || 'Registration failed. Please try again.';
      setGeneralError(errorMsg);
      console.error('Registration error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Step 1: Account Type Selection
  if (step === 'account-type') {
    return (
      <div className="register-container">
        <div className="register-card fade-in">
          <div className="register-header">
            <h1>Create Your Account</h1>
            <p>Choose the type of account that suits you best</p>
          </div>

          <div className="account-type-selection">
            <button
              className="account-type-btn"
              onClick={() => handleAccountTypeSelect(false)}
            >
              <User size={48} />
              <h3>Private Account</h3>
              <p>For individuals and freelancers</p>
              <ul className="type-benefits">
                <li>✓ Personal dashboard</li>
                <li>✓ Project management</li>
                <li>✓ Email verification</li>
              </ul>
            </button>

            <button
              className="account-type-btn"
              onClick={() => handleAccountTypeSelect(true)}
            >
              <Building2 size={48} />
              <h3>Company Account</h3>
              <p>For businesses and enterprises</p>
              <ul className="type-benefits">
                <li>✓ All features + company tools</li>
                <li>✓ Team management</li>
                <li>✓ Billing & invoicing</li>
              </ul>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Step 2: Registration Form
  if (step === 'form') {
    return (
      <div className="register-container">
        <div className="register-card fade-in">
          <div className="register-header">
            <h1>Register {formData.is_company ? 'Company' : 'Personal'} Account</h1>
            <button
              className="step-back-btn"
              onClick={() => setStep('account-type')}
              type="button"
            >
              ← Back
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {generalError && (
              <div className="error-box">
                <AlertCircle size={20} />
                <span>{generalError}</span>
              </div>
            )}

            {/* Personal Information Section */}
            <div className="form-section">
              <h2>Personal Information</h2>

              <div className="form-row">
                <div className="form-group">
                  <label>First Name *</label>
                  <input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    placeholder="John"
                    className={errors.first_name ? 'error' : ''}
                  />
                  {errors.first_name && <span className="error-text">{errors.first_name}</span>}
                </div>

                <div className="form-group">
                  <label>Last Name *</label>
                  <input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    placeholder="Doe"
                    className={errors.last_name ? 'error' : ''}
                  />
                  {errors.last_name && <span className="error-text">{errors.last_name}</span>}
                </div>
              </div>

              <div className="form-group">
                <label>Email *</label>
                <div className="input-with-status">
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleEmailChange}
                    placeholder="john@example.com"
                    className={errors.email ? 'error' : ''}
                  />
                  {emailAvailabilityStatus === 'checking' && <span className="status-checking">Checking...</span>}
                  {emailAvailabilityStatus === 'available' && <CheckCircle className="status-available" size={18} />}
                  {emailAvailabilityStatus === 'taken' && <AlertCircle className="status-taken" size={18} />}
                </div>
                {errors.email && <span className="error-text">{errors.email}</span>}
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Password *</label>
                  <div className="input-with-toggle">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      placeholder="••••••••"
                      className={errors.password ? 'error' : ''}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="toggle-btn"
                    >
                      {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  {formData.password && (
                    <div className="password-strength">
                      <div className="strength-bar">
                        <div
                          className={`strength-fill strength-${
                            passwordStrength < 30 ? 'weak' : passwordStrength < 60 ? 'fair' : passwordStrength < 85 ? 'good' : 'strong'
                          }`}
                          style={{ width: `${passwordStrength}%` }}
                        ></div>
                      </div>
                      <span className={`strength-label strength-${
                        passwordStrength < 30 ? 'weak' : passwordStrength < 60 ? 'fair' : passwordStrength < 85 ? 'good' : 'strong'
                      }`}>
                        {registrationService.getPasswordStrengthLabel(formData.password)}
                      </span>
                    </div>
                  )}
                  {errors.password && <span className="error-text">{errors.password}</span>}
                </div>

                <div className="form-group">
                  <label>Confirm Password *</label>
                  <div className="input-with-toggle">
                    <input
                      type={showPasswordConfirm ? 'text' : 'password'}
                      name="password_confirm"
                      value={formData.password_confirm}
                      onChange={handleInputChange}
                      placeholder="••••••••"
                      className={errors.password_confirm ? 'error' : ''}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPasswordConfirm(!showPasswordConfirm)}
                      className="toggle-btn"
                    >
                      {showPasswordConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  {errors.password_confirm && <span className="error-text">{errors.password_confirm}</span>}
                </div>
              </div>

              <div className="form-group">
                <label>Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  placeholder="+48 123 456 789"
                  className={errors.phone ? 'error' : ''}
                />
                {errors.phone && <span className="error-text">{errors.phone}</span>}
              </div>
            </div>

            {/* Address Section */}
            <div className="form-section">
              <h2>Address</h2>

              <div className="form-group">
                <label>Street & Building/Apartment Number *</label>
                <input
                  type="text"
                  name="street"
                  value={formData.street}
                  onChange={handleInputChange}
                  placeholder="123 Main Street, Apt 4B"
                  className={errors.street ? 'error' : ''}
                />
                {errors.street && <span className="error-text">{errors.street}</span>}
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Postal Code *</label>
                  <input
                    type="text"
                    name="postal_code"
                    value={formData.postal_code}
                    onChange={handleInputChange}
                    placeholder="XX-XXX"
                    className={errors.postal_code ? 'error' : ''}
                  />
                  {errors.postal_code && <span className="error-text">{errors.postal_code}</span>}
                </div>

                <div className="form-group">
                  <label>City *</label>
                  <input
                    type="text"
                    name="city"
                    value={formData.city}
                    onChange={handleInputChange}
                    placeholder="Warsaw"
                    className={errors.city ? 'error' : ''}
                  />
                  {errors.city && <span className="error-text">{errors.city}</span>}
                </div>

                <div className="form-group">
                  <label>Country *</label>
                  <select
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    className={errors.country ? 'error' : ''}
                  >
                    <option value="PL">Poland</option>
                    <option value="DE">Germany</option>
                    <option value="FR">France</option>
                    <option value="GB">United Kingdom</option>
                    <option value="US">United States</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Company Section (if applicable) */}
            {formData.is_company && formData.company_details && (
              <div className="form-section">
                <h2>Company Information</h2>

                <div className="form-group">
                  <label>Company Name *</label>
                  <input
                    type="text"
                    name="company_name"
                    value={formData.company_details.company_name}
                    onChange={(e) => handleInputChange(e, 'company')}
                    placeholder="ABC Corporation"
                    className={errors.company_name ? 'error' : ''}
                  />
                  {errors.company_name && <span className="error-text">{errors.company_name}</span>}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>NIP (Tax Identification Number) *</label>
                    <input
                      type="text"
                      name="nip"
                      value={formData.company_details.nip}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="1234567890"
                      className={errors.nip ? 'error' : ''}
                    />
                    {errors.nip && <span className="error-text">{errors.nip}</span>}
                  </div>

                  <div className="form-group">
                    <label>REGON</label>
                    <input
                      type="text"
                      name="regon"
                      value={formData.company_details.regon}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="123456789"
                    />
                  </div>

                  <div className="form-group">
                    <label>KRS (optional)</label>
                    <input
                      type="text"
                      name="krs"
                      value={formData.company_details.krs}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="0000000000"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Company Address *</label>
                  <input
                    type="text"
                    name="company_address"
                    value={formData.company_details.company_address}
                    onChange={(e) => handleInputChange(e, 'company')}
                    placeholder="456 Business Ave"
                    className={errors.company_address ? 'error' : ''}
                  />
                  {errors.company_address && <span className="error-text">{errors.company_address}</span>}
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Postal Code</label>
                    <input
                      type="text"
                      name="company_postal_code"
                      value={formData.company_details.company_postal_code}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="XX-XXX"
                    />
                  </div>

                  <div className="form-group">
                    <label>City</label>
                    <input
                      type="text"
                      name="company_city"
                      value={formData.company_details.company_city}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="Warsaw"
                    />
                  </div>

                  <div className="form-group">
                    <label>Country</label>
                    <select
                      name="company_country"
                      value={formData.company_details.company_country}
                      onChange={(e) => handleInputChange(e, 'company')}
                    >
                      <option value="PL">Poland</option>
                      <option value="DE">Germany</option>
                      <option value="FR">France</option>
                      <option value="GB">United Kingdom</option>
                      <option value="US">United States</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Contact Person *</label>
                    <input
                      type="text"
                      name="contact_person"
                      value={formData.company_details.contact_person}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="John Owner"
                      className={errors.contact_person ? 'error' : ''}
                    />
                    {errors.contact_person && <span className="error-text">{errors.contact_person}</span>}
                  </div>

                  <div className="form-group">
                    <label>Company Phone</label>
                    <input
                      type="tel"
                      name="company_phone"
                      value={formData.company_details.company_phone}
                      onChange={(e) => handleInputChange(e, 'company')}
                      placeholder="+48 123 456 789"
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Company Email</label>
                  <input
                    type="email"
                    name="company_email"
                    value={formData.company_details.company_email}
                    onChange={(e) => handleInputChange(e, 'company')}
                    placeholder="company@example.com"
                  />
                </div>
              </div>
            )}

            {/* Terms & Conditions */}
            <div className="form-section">
              <h2>Agreement</h2>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="accept_terms"
                    checked={formData.accept_terms}
                    onChange={handleInputChange}
                  />
                  <span>I accept the Terms and Conditions *</span>
                </label>
                {errors.accept_terms && <span className="error-text">{errors.accept_terms}</span>}
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="accept_gdpr"
                    checked={formData.accept_gdpr}
                    onChange={handleInputChange}
                  />
                  <span>I accept GDPR and Privacy Policy *</span>
                </label>
                {errors.accept_gdpr && <span className="error-text">{errors.accept_gdpr}</span>}
              </div>
            </div>

            <button
              type="submit"
              className="submit-btn"
              disabled={loading || emailAvailabilityStatus !== 'available'}
            >
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // Step 3: Success Message
  if (step === 'success') {
    return (
      <div className="register-container">
        <div className="register-card fade-in success-card">
          <div className="success-icon">
            <CheckCircle size={64} color="#28a745" />
          </div>
          <h1>Account Created Successfully!</h1>
          <p>We've sent a verification email to:</p>
          <p className="success-email">{successEmail}</p>
          <p>Please click the link in the email to verify your account and complete your registration.</p>
          {formData.is_company && (
            <div className="company-notice">
              <p>
                <strong>Company Account:</strong> Your company account is pending verification. Our team will review your information and send you a confirmation email soon.
              </p>
            </div>
          )}
          <div className="success-actions">
            <p>Redirecting to login page...</p>
          </div>
        </div>
      </div>
    );
  }

  return null;
};
