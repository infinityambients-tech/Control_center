import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Wallet,
  Repeat,
  Map,
  Activity,
  Settings,
  Boxes,
  Shield,
  Layers
} from 'lucide-react';

const navItems = [
  { icon: LayoutDashboard, label: 'Portfolio', path: '/' },
  { icon: Wallet, label: 'Finance', path: '/finance' },
  { icon: Repeat, label: 'Subscriptions', path: '/subscriptions' },
  { icon: Map, label: 'Roadmap', path: '/roadmap' },
  { icon: Activity, label: 'Deployments', path: '/deployments' },
  { icon: Layers, label: 'Plans & Limits', path: '/plans' },
  { icon: Shield, label: 'Security', path: '/audit' },
  { icon: Boxes, label: 'Updates', path: '/updates' },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <Boxes size={24} color="#0070f3" />
        <span className="logo-text">Control Center</span>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <NavLink to="/settings" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <Settings size={20} />
          <span>Settings</span>
        </NavLink>
        <button
          className="nav-item logout-btn"
          onClick={async () => {
            const { authService } = await import('../services/authService');
            await authService.logout();
            window.location.href = '/#/login';
            window.location.reload();
          }}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Log out</span>
        </button>
      </div>

      <style>{`
        .sidebar {
          width: var(--sidebar-width);
          height: 100vh;
          background-color: var(--bg-card);
          border-right: 1px solid var(--border);
          display: flex;
          flex-direction: column;
          padding: 24px 16px;
        }

        .sidebar-header {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 0 12px 32px;
        }

        .logo-text {
          font-weight: 700;
          font-size: 1.1rem;
          letter-spacing: -0.02em;
        }

        .sidebar-nav {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .nav-item {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 10px 12px;
          border-radius: 8px;
          color: var(--text-secondary);
          text-decoration: none;
          transition: all 0.2s ease;
          font-size: 0.95rem;
        }

        .nav-item:hover {
          background-color: var(--glass);
          color: var(--text-primary);
        }

        .nav-item.active {
          background-color: rgba(0, 112, 243, 0.1);
          color: var(--accent);
          font-weight: 500;
        }

        .sidebar-footer {
          margin-top: auto;
          border-top: 1px solid var(--border);
          padding-top: 16px;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .logout-btn {
          background: none;
          border: none;
          width: 100%;
          text-align: left;
          cursor: pointer;
          font-family: inherit;
        }
        
        .logout-btn:hover {
          background-color: rgba(255, 82, 82, 0.1) !important;
          color: #ff5252 !important;
        }
      `}</style>
    </aside>
  );
};
