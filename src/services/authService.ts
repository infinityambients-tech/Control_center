const API_BASE = '/api/v1';

export const authService = {
    async login(email: string, password: string): Promise<{ success: boolean; message?: string }> {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 expects username
        formData.append('password', password);

        try {
            const response = await fetch(`${API_BASE}/auth/login/access-token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
                credentials: 'include' // ensure cookies are set/used
            });

            if (response.ok) {
                return { success: true };
            }

            // Attempt to read error details from backend
            let detail = 'Login failed';
            try {
                const err = await response.json();
                detail = err.detail || err.message || detail;
            } catch (e) {
                // ignore JSON parse errors
            }

            return { success: false, message: detail };
        } catch (err) {
            console.error('Login error', err);
            return { success: false, message: 'Network error during login' };
        }
    },

    async refreshToken(): Promise<boolean> {
        try {
            const response = await fetch(`${API_BASE}/auth/refresh`, {
                method: 'POST',
                credentials: 'include'
            });
            if (response.ok) {
                return true;
            }
            return false;
        } catch (err) {
            return false;
        }
    },

    async logout(): Promise<void> {
        // Clear server-side cookies first
        try {
            await fetch(`${API_BASE}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
        } catch (err) {
            console.error('Logout error', err);
        }
        // Then clear any client-side state
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    isAuthenticated(): boolean {
        // Deprecated: use whoami() async check for cookie-based auth
        return !!localStorage.getItem('access_token');
    },

    async whoami(): Promise<{ authenticated: boolean; user?: any }> {
        try {
            const resp = await fetch(`${API_BASE}/auth/me`, { credentials: 'include' });
            if (resp.ok) {
                const user = await resp.json();
                return { authenticated: true, user };
            }
            return { authenticated: false };
        } catch (e) {
            return { authenticated: false };
        }
    },
};
