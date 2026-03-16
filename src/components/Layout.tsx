import React, { useEffect, useState } from 'react';
import { Sidebar } from './Sidebar';
import { realtimeService } from '../services/realtimeService';

interface LayoutProps {
    children: React.ReactNode;
    title: string;
}

export const Layout: React.FC<LayoutProps> = ({ children, title }) => {
  const [connected, setConnected] = useState<boolean>(false);

  useEffect(() => {
    const onConnected = () => setConnected(true);
    const onDisconnected = () => setConnected(false);
    realtimeService.on('connected', onConnected);
    realtimeService.on('disconnected', onDisconnected);
    // initial state
    setConnected(realtimeService.isConnected);
    return () => {
      realtimeService.off('connected', onConnected);
      realtimeService.off('disconnected', onDisconnected);
    };
  }, []);
    return (
        <div className="layout">
            <Sidebar />
            <main className="main-content">
                <header className="content-header">
                    <h1 className="page-title">{title}</h1>
                    <div className="header-actions">
                      {/* Realtime connection indicator */}
                      <div style={{display:'flex', alignItems:'center', gap:8}}>
                        <div style={{width:10, height:10, borderRadius:10, background: connected ? '#28a745' : '#6c757d'}} />
                        <span style={{fontSize:12, color:'var(--text-secondary)'}}>{connected ? 'Realtime: connected' : 'Realtime: offline'}</span>
                      </div>
                    </div>
                </header>
                <div className="content-body fade-in">
                    {children}
                </div>
            </main>

            <style>{`
        .layout {
          display: flex;
          width: 100%;
          height: 100vh;
          background-color: var(--bg-dark);
        }

        .main-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        .content-header {
          height: 80px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 40px;
          border-bottom: 1px solid var(--border);
        }

        .page-title {
          font-size: 1.5rem;
          font-weight: 700;
          letter-spacing: -0.02em;
        }

        .content-body {
          flex: 1;
          padding: 40px;
          overflow-y: auto;
        }
      `}</style>
        </div>
    );
};
