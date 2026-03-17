const API_BASE = '/api/v1';

const getAuthToken = () => localStorage.getItem('access_token');

export interface AuditLog {
    id: number;
    user_id: number | null;
    action: string;
    entity: string | null;
    entity_id: string | null;
    timestamp: string;
    ip_address: string | null;
    metadata_json: any;
}

export const auditService = {
    async getLogs(limit = 100): Promise<AuditLog[]> {
        const response = await fetch(`${API_BASE}/audit/?limit=${limit}`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return [];
        return await response.json();
    }
};
