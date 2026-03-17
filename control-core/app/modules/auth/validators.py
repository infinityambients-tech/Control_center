"""
Validation utilities for registration and authentication
"""
import re
from typing import Tuple

# ============== Email Validation ==============

def validate_email_format(email: str) -> bool:
    """Validate email format using RFC 5322 pattern"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ============== Password Validation ==============

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 digit
    - At least 1 special character
    
    Returns: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least 1 uppercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least 1 digit"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least 1 special character"
    
    return True, "Password is strong"

# ============== NIP Validation (Poland) ==============

def validate_nip(nip: str) -> Tuple[bool, str]:
    """
    Validate Polish NIP (Numer Identyfikacji Podatkowej).
    
    Rules:
    - 10 digits
    - Valid checksum (Luhn algorithm with weights)
    
    Returns: (is_valid, message)
    """
    # Remove common separators
    nip = re.sub(r'[-\s]', '', nip)
    
    # Check if 10 digits
    if not re.match(r'^\d{10}$', nip):
        return False, "NIP must be exactly 10 digits"
    
    # NIP checksum validation
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = 0
    
    for i, digit in enumerate(nip[:9]):
        checksum += int(digit) * weights[i]
    
    control = (10 - (checksum % 10)) % 10
    
    if int(nip[9]) != control:
        return False, "NIP checksum is invalid"
    
    return True, "NIP is valid"

# ============== REGON Validation (Poland) ==============

def validate_regon(regon: str) -> Tuple[bool, str]:
    """
    Validate Polish REGON (Rejestr Gospodarki Narodowej).
    
    Rules:
    - 9 digits (business) or 14 digits (with divisions)
    - Valid checksum
    
    Returns: (is_valid, message)
    """
    regon = re.sub(r'[-\s]', '', regon)
    
    if not re.match(r'^(\d{9}|\d{14})$', regon):
        return False, "REGON must be 9 or 14 digits"
    
    # Checksum validation for REGON
    weights_9 = [8, 9, 2, 3, 4, 5, 6, 7, 0]
    weights_14 = [1, 2, 4, 8, 5, 0, 9, 7, 6, 4, 2, 3, 5, 9]
    
    weights = weights_14 if len(regon) == 14 else weights_9
    checksum = 0
    
    for i, digit in enumerate(regon[:-1]):
        checksum += int(digit) * weights[i]
    
    control = (10 - (checksum % 10)) % 10
    
    if int(regon[-1]) != control:
        return False, "REGON checksum is invalid"
    
    return True, "REGON is valid"

# ============== Document Upload Validation ==============

def validate_document_upload(filename: str, file_size: int) -> Tuple[bool, str]:
    """
    Validate document for company registration.
    
    Rules:
    - Allowed formats: PDF, JPG, PNG
    - Max size: 5 MB
    
    Returns: (is_valid, message)
    """
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
    max_size = 5 * 1024 * 1024  # 5 MB
    
    # Check extension
    ext = '.' + filename.split('.')[-1].lower()
    if ext not in allowed_extensions:
        return False, f"Document must be PDF, JPG, or PNG (got .{ext})"
    
    # Check size
    if file_size > max_size:
        return False, f"Document must be smaller than 5 MB (got {file_size / 1024 / 1024:.2f} MB)"
    
    return True, "Document is valid"

# ============== Form Data Validation ==============

def validate_registration_form(data) -> Tuple[bool, dict]:
    """
    Validate complete registration form.
    
    Returns: (is_valid, errors_dict)
    """
    errors = {}
    
    # Email validation
    if not validate_email_format(data.email):
        errors['email'] = "Invalid email format"
    
    # Password validation
    is_strong, msg = validate_password_strength(data.password)
    if not is_strong:
        errors['password'] = msg
    
    # Password confirmation
    if data.password != data.password_confirm:
        errors['password_confirm'] = "Passwords do not match"
    
    # First/Last name
    if not data.first_name or len(data.first_name.strip()) < 2:
        errors['first_name'] = "First name must be at least 2 characters"
    
    if not data.last_name or len(data.last_name.strip()) < 2:
        errors['last_name'] = "Last name must be at least 2 characters"
    
    # Address validation
    if not data.street or len(data.street.strip()) < 3:
        errors['street'] = "Street must be at least 3 characters"
    
    if not data.postal_code or not re.match(r'^\d{2}-\d{3}$', data.postal_code):
        errors['postal_code'] = "Postal code must be in format XX-XXX"
    
    if not data.city or len(data.city.strip()) < 2:
        errors['city'] = "City must be at least 2 characters"
    
    if not data.country or len(data.country.strip()) < 2:
        errors['country'] = "Country must be at least 2 characters"
    
    # Phone validation (if provided)
    if data.phone:
        if not re.match(r'^\+?[\d\s\-()]{8,}$', data.phone):
            errors['phone'] = "Invalid phone number format"
    
    # Company validation (if is_company)
    if data.is_company and data.company_details:
        company = data.company_details
        
        if not company.company_name or len(company.company_name.strip()) < 3:
            errors['company_name'] = "Company name must be at least 3 characters"
        
        # NIP validation
        nip_valid, nip_msg = validate_nip(company.nip)
        if not nip_valid:
            errors['nip'] = nip_msg
        
        # REGON validation (if provided)
        if company.regon:
            regon_valid, regon_msg = validate_regon(company.regon)
            if not regon_valid:
                errors['regon'] = regon_msg
        
        if not company.company_address or len(company.company_address.strip()) < 3:
            errors['company_address'] = "Company address must be at least 3 characters"
        
        if not company.contact_person or len(company.contact_person.strip()) < 2:
            errors['contact_person'] = "Contact person must be at least 2 characters"
    
    # Terms acceptance
    if not data.accept_terms:
        errors['accept_terms'] = "You must accept terms and conditions"
    
    if not data.accept_gdpr:
        errors['accept_gdpr'] = "You must accept GDPR policy"
    
    return len(errors) == 0, errors

# ============== Postal Code Validation ==============

def validate_postal_code(postal_code: str, country: str = "PL") -> Tuple[bool, str]:
    """
    Validate postal code based on country.
    
    Returns: (is_valid, message)
    """
    if country == "PL":
        # Polish format: XX-XXX
        if re.match(r'^\d{2}-\d{3}$', postal_code):
            return True, "Valid Polish postal code"
        return False, "Polish postal code must be in format XX-XXX"
    
    # Generic validation for other countries
    if len(postal_code) >= 3:
        return True, "Valid postal code"
    
    return False, "Invalid postal code"

# ============== Username/Email Format Utilities ==============

def sanitize_input(value: str) -> str:
    """Remove potentially dangerous characters from input"""
    if not value:
        return ""
    # Remove null bytes and control characters
    return value.replace('\x00', '').strip()

def get_password_strength_percentage(password: str) -> int:
    """
    Calculate password strength as percentage (0-100).
    Used for frontend strength indicator.
    """
    score = 0
    
    if len(password) >= 8:
        score += 20
    if len(password) >= 12:
        score += 10
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'[0-9]', password):
        score += 15
    if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        score += 10
    
    return min(score, 100)
