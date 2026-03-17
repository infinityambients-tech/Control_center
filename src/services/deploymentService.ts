const API_BASE = '/api/v1';

export type DeploymentStatus = 'queued' | 'building' | 'deployed' | 'failed' | 'rolled_back';
export type EnvironmentType = 'development' | 'staging' | 'production';

export interface Deployment {
    id: string;
    project_id: string;
    environment: EnvironmentType;
    version?: string;
    commit_hash?: string;
    status: DeploymentStatus;
    logs?: string;
    deployed_by?: string;
    deployed_at: string;
}

export const deploymentService = {
    async getDeployments(): Promise<Deployment[]> {
        try {
            const response = await fetch(`${API_BASE}/deployments`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`
                }
            });
            if (response.ok) return await response.json();
            return [];
        } catch (error) {
            console.error('Failed to load deployments:', error);
            return [];
        }
    },

    async triggerDeployment(projectId: string, environment: EnvironmentType): Promise<Deployment | null> {
        try {
            const response = await fetch(`${API_BASE}/deployments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token') || ''}`
                },
                body: JSON.stringify({
                    project_id: projectId,
                    environment: environment,
                    version: '1.0.0', // default or dynamic
                    commit_hash: Math.random().toString(36).substring(7) // mock hash
                })
            });
            if (response.ok) return await response.json();
            return null;
        } catch (error) {
            console.error('Failed to trigger deployment:', error);
            return null;
        }
    }
};
