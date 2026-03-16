/**
 * Registration Service
 * Handles API calls for user registration and account setup
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

interface RegistrationData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  password_confirm: string;
  phone?: string;
  street: string;
  postal_code: string;
  city: string;
  country: string;
  is_company: boolean;
  company_details?: CompanyDetails;
  accept_terms: boolean;
  accept_gdpr: boolean;
}

interface CompanyDetails {
  company_name: string;
  nip: string;
  regon?: string;
  krs?: string;
  company_address: string;
  company_postal_code?: string;
  company_city?: string;
  company_country?: string;
  contact_person: string;
  company_phone?: string;
  company_email?: string;
}

interface RegisterResponse {
  success: boolean;
  message: string;
  status: string;
  user_id?: string;
}

interface EmailCheckResponse {
  available: boolean;
  message: string;
}

interface VerifyEmailResponse {
  success: boolean;
  message: string;
  status?: string;
}

export const registrationService = {
  /**
   * Register a new user account
   */
  async register(data: RegistrationData): Promise<RegisterResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  /**
   * Check if email is available for registration
   */
  async checkEmailAvailability(email: string): Promise<EmailCheckResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/check-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        throw new Error('Email check failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Email check error:', error);
      throw error;
    }
  },

  /**
   * Verify email with token
   */
  async verifyEmail(token: string): Promise<VerifyEmailResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Verification failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Email verification error:', error);
      throw error;
    }
  },

  /**
   * Resend verification email
   */
  async resendVerificationEmail(email: string): Promise<VerifyEmailResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/resend-verification`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to resend verification email');
      }

      return await response.json();
    } catch (error) {
      console.error('Resend verification error:', error);
      throw error;
    }
  },

  /**
   * Validate registration form on frontend (mirrors backend validation)
   */
  validateForm(data: RegistrationData): Record<string, string> {
    const errors: Record<string, string> = {};

    // Email validation
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(data.email)) {
      errors.email = 'Invalid email format';
    }

    // Password validation
    if (data.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    }
    if (!/[A-Z]/.test(data.password)) {
      errors.password = 'Password must contain at least 1 uppercase letter';
    }
    if (!/[0-9]/.test(data.password)) {
      errors.password = 'Password must contain at least 1 digit';
    }
    if (!/[!@#$%^&*()_+\-=\[\]{};:'",./<>?\\|`~]/.test(data.password)) {
      errors.password = 'Password must contain at least 1 special character';
    }

    if (data.password !== data.password_confirm) {
      errors.password_confirm = 'Passwords do not match';
    }

    // Name validation
    if (!data.first_name || data.first_name.trim().length < 2) {
      errors.first_name = 'First name must be at least 2 characters';
    }
    if (!data.last_name || data.last_name.trim().length < 2) {
      errors.last_name = 'Last name must be at least 2 characters';
    }

    // Address validation
    if (!data.street || data.street.trim().length < 3) {
      errors.street = 'Street must be at least 3 characters';
    }
    if (!data.postal_code || !/^\d{2}-\d{3}$/.test(data.postal_code)) {
      errors.postal_code = 'Postal code must be in format XX-XXX';
    }
    if (!data.city || data.city.trim().length < 2) {
      errors.city = 'City must be at least 2 characters';
    }
    if (!data.country || data.country.trim().length < 2) {
      errors.country = 'Country must be at least 2 characters';
    }

    // Phone validation (optional)
    if (data.phone && !/^\+?[\d\s\-()]{8,}$/.test(data.phone)) {
      errors.phone = 'Invalid phone number format';
    }

    // Company validation
    if (data.is_company && data.company_details) {
      const company = data.company_details;

      if (!company.company_name || company.company_name.trim().length < 3) {
        errors.company_name = 'Company name must be at least 3 characters';
      }

      // NIP validation
      const nipValid = this.validateNIP(company.nip);
      if (!nipValid.valid) {
        errors.nip = nipValid.message;
      }

      // REGON validation (if provided)
      if (company.regon) {
        const regonValid = this.validateREGON(company.regon);
        if (!regonValid.valid) {
          errors.regon = regonValid.message;
        }
      }

      if (!company.company_address || company.company_address.trim().length < 3) {
        errors.company_address = 'Company address must be at least 3 characters';
      }

      if (!company.contact_person || company.contact_person.trim().length < 2) {
        errors.contact_person = 'Contact person must be at least 2 characters';
      }
    }

    // Terms acceptance
    if (!data.accept_terms) {
      errors.accept_terms = 'You must accept terms and conditions';
    }
    if (!data.accept_gdpr) {
      errors.accept_gdpr = 'You must accept GDPR policy';
    }

    return errors;
  },

  /**
   * Validate Polish NIP (Numer Identyfikacji Podatkowej)
   */
  validateNIP(nip: string): { valid: boolean; message: string } {
    // Remove common separators
    const cleanNIP = nip.replace(/[-\s]/g, '');

    // Check if 10 digits
    if (!/^\d{10}$/.test(cleanNIP)) {
      return { valid: false, message: 'NIP must be exactly 10 digits' };
    }

    // NIP checksum validation
    const weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3];
    let checksum = 0;

    for (let i = 0; i < 9; i++) {
      checksum += parseInt(cleanNIP[i]) * weights[i];
    }

    const control = (10 - (checksum % 10)) % 10;

    if (parseInt(cleanNIP[9]) !== control) {
      return { valid: false, message: 'NIP checksum is invalid' };
    }

    return { valid: true, message: 'NIP is valid' };
  },

  /**
   * Validate Polish REGON (Rejestr Gospodarki Narodowej)
   */
  validateREGON(regon: string): { valid: boolean; message: string } {
    const cleanREGON = regon.replace(/[-\s]/g, '');

    if (!/^(\d{9}|\d{14})$/.test(cleanREGON)) {
      return { valid: false, message: 'REGON must be 9 or 14 digits' };
    }

    const weights9 = [8, 9, 2, 3, 4, 5, 6, 7, 0];
    const weights14 = [1, 2, 4, 8, 5, 0, 9, 7, 6, 4, 2, 3, 5, 9];

    const weights = cleanREGON.length === 14 ? weights14 : weights9;
    let checksum = 0;

    for (let i = 0; i < cleanREGON.length - 1; i++) {
      checksum += parseInt(cleanREGON[i]) * weights[i];
    }

    const control = (10 - (checksum % 10)) % 10;

    if (parseInt(cleanREGON[cleanREGON.length - 1]) !== control) {
      return { valid: false, message: 'REGON checksum is invalid' };
    }

    return { valid: true, message: 'REGON is valid' };
  },

  /**
   * Calculate password strength percentage
   */
  getPasswordStrength(password: string): number {
    let score = 0;

    if (password.length >= 8) score += 20;
    if (password.length >= 12) score += 10;
    if (/[a-z]/.test(password)) score += 15;
    if (/[A-Z]/.test(password)) score += 15;
    if (/[0-9]/.test(password)) score += 15;
    if (/[!@#$%^&*()_+\-=\[\]{};:'",./<>?\\|`~]/.test(password)) score += 10;

    return Math.min(score, 100);
  },

  /**
   * Get password strength label
   */
  getPasswordStrengthLabel(password: string): string {
    const strength = this.getPasswordStrength(password);
    if (strength < 30) return 'Weak';
    if (strength < 60) return 'Fair';
    if (strength < 85) return 'Good';
    return 'Strong';
  },
};
