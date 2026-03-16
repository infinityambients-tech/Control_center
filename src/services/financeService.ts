const API_BASE = 'http://localhost:8000/api/v1';

const getAuthToken = () => localStorage.getItem('access_token');

export interface PaymentSnapshot {
    id: number;
    project_id: string;
    external_payment_id: string;
    amount: number;
    currency: string;
    status: string;
    created_at: string;
}

export interface FinanceSummary {
    total_revenue: number;
    mrr: number;
    mrr_growth: number;
    churn_rate: number;
    ltv: number;
}

export const financeService = {
    async getSummary(): Promise<FinanceSummary | null> {
        const response = await fetch(`${API_BASE}/finance/summary`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return null;
        return await response.json();
    },

    async getRecentPayments(limit = 50): Promise<PaymentSnapshot[]> {
        const response = await fetch(`${API_BASE}/finance/payments?limit=${limit}`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return [];
        return await response.json();
    }
};
