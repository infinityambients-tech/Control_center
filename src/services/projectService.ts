import type { Project } from '../types/electron';

const API_BASE = '/api/v1';

// Helper to get token (to be implemented better with authService)
const getAuthToken = () => localStorage.getItem('access_token');

export const projectService = {
    async getAll(): Promise<Project[]> {
        const response = await fetch(`${API_BASE}/projects/`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return [];
        return await response.json();
    },

    async add(project: Omit<Project, 'id' | 'created_at' | 'status'>): Promise<boolean> {
        const response = await fetch(`${API_BASE}/projects/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify(project)
        });
        return response.ok;
    },

    async delete(id: string): Promise<boolean> {
        const response = await fetch(`${API_BASE}/projects/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        return response.ok;
    },

    // These will now call the centralized sync/secret management
    async triggerSync(): Promise<boolean> {
        const response = await fetch(`${API_BASE}/analytics/sync`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        return response.ok;
    },

    async getSummary() {
        const response = await fetch(`${API_BASE}/analytics/summary`, {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        if (!response.ok) return null;
        return await response.json();
    }
};
