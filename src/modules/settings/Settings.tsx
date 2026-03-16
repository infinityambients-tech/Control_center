import React, { useState } from 'react';
import { Layout } from '../../components/Layout';
import { User, Bell, Shield, Sliders } from 'lucide-react';
import { AccountSettings } from './AccountSettings';

export const Settings: React.FC = () => {
    const [activeTab, setActiveTab] = useState('account');

    const renderContent = () => {
        switch (activeTab) {
            case 'account':
                return <AccountSettings />;
            default:
                return (
                    <div className="placeholder-pane fade-in">
                        <h2>Under Construction</h2>
                        <p>This settings tab is being developed.</p>
                    </div>
                );
        }
    };

    return (
        <Layout title="Settings">
            <div className="settings-container">

                <aside className="settings-sidebar">
                    <nav>
                        <button
                            className={`settings-nav-item ${activeTab === 'account' ? 'active' : ''}`}
                            onClick={() => setActiveTab('account')}
                        >
                            <User size={18} />
                            Account
                        </button>
                        <button
                            className={`settings-nav-item ${activeTab === 'general' ? 'active' : ''}`}
                            onClick={() => setActiveTab('general')}
                        >
                            <Sliders size={18} />
                            General
                        </button>
                        <button
                            className={`settings-nav-item ${activeTab === 'notifications' ? 'active' : ''}`}
                            onClick={() => setActiveTab('notifications')}
                        >
                            <Bell size={18} />
                            Notifications
                        </button>
                        <button
                            className={`settings-nav-item ${activeTab === 'security' ? 'active' : ''}`}
                            onClick={() => setActiveTab('security')}
                        >
                            <Shield size={18} />
                            Security
                        </button>
                    </nav>
                </aside>

                <main className="settings-content">
                    {renderContent()}
                </main>

            </div>

            <style>{`
        .settings-container {
          display: flex;
          gap: 40px;
          padding-top: 12px;
          height: calc(100vh - 140px);
        }

        .settings-sidebar {
          width: 200px;
          flex-shrink: 0;
          border-right: 1px solid var(--border);
          padding-right: 20px;
        }

        .settings-sidebar nav {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .settings-nav-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 10px 12px;
          background: transparent;
          border: none;
          color: var(--text-secondary);
          font-size: 0.95rem;
          text-align: left;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .settings-nav-item:hover {
          background: rgba(255, 255, 255, 0.05);
          color: var(--text-primary);
        }

        .settings-nav-item.active {
          background: rgba(0, 112, 243, 0.1);
          color: var(--accent);
          font-weight: 500;
        }

        .settings-content {
          flex: 1;
          overflow-y: auto;
          overflow-x: hidden;
        }

        .placeholder-pane {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100%;
          color: var(--text-secondary);
          border: 1px dashed var(--border);
          border-radius: 12px;
        }
      `}</style>
        </Layout>
    );
};

export default Settings;
