const API_BASE = '/api/v1';

const getAuthToken = () => localStorage.getItem('access_token');

export interface SubscriptionSnapshot {
    id: number;
    project_id: string;
    external_id: string;
    plan: string;
    status: string;
    current_period_end: string;
    created_at: string;
}

export interface SubscriptionSummary {
    total_active: number;
    plans_distribution: Record<string, number>;
    churned_count: number;
}

export const subscriptionService = {
    async getSummary(): Promise<SubscriptionSummary | null> {
        const response = await fetch(`${API_BASE}/subscriptions/summary`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return null;
        return await response.json();
    },

    async getAll(limit = 100): Promise<SubscriptionSnapshot[]> {
        const response = await fetch(`${API_BASE}/subscriptions/?limit=${limit}`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return [];
        return await response.json();
    }
};
