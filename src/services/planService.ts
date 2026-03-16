const API_BASE = 'http://localhost:8000/api/v1';

export interface Plan {
    id: string;
    name: string;
    monthly_price: number;
    yearly_price: number;
    max_projects: number;
    max_users: number;
    max_storage_gb: number;
    priority_support: boolean;
    created_at: string;
}

export const planService = {
    async getPlans(): Promise<Plan[]> {
        try {
            const response = await fetch(`${API_BASE}/plans`, {
                headers: {
                    // Try to grab token from local storage if available for authorization testing
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`
                },
                credentials: 'omit' // public endpoint or standard auth
            });
            if (response.ok) {
                return await response.json();
            }
            return [];
        } catch (error) {
            console.error('Failed to load plans:', error);
            return [];
        }
    }
};
