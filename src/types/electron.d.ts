export interface Project {
    id: string;
    name: string;
    type?: string;
    api_base_url?: string;
    payment_provider?: string;
    status: 'active' | 'inactive' | 'archived';
    created_at: string;
}

export interface ElectronAPI {
    // Secrets
    saveSecret: (data: { service: string; account: string; password: string }) => Promise<boolean>;
    getSecret: (data: { service: string; account: string }) => Promise<string | null>;
    deleteSecret: (data: { service: string; account: string }) => Promise<boolean>;
}

declare global {
    interface Window {
        api: ElectronAPI;
    }
}
