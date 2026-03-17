import React, { useEffect, useState } from 'react';
import { Layout } from '../../components/Layout';
import { Plus, Trash2, ExternalLink, Activity, DollarSign, Users } from 'lucide-react';
import { projectService } from '../../services/projectService';
import type { Project } from '../../types/electron';
import { AddProjectModal } from './AddProjectModal';

export const Portfolio: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [summary, setSummary] = useState({ total_mrr: 0, total_revenue_today: 0, total_active_subs: 0 });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [projectsData, summaryData] = await Promise.all([
        projectService.getAll(),
        projectService.getSummary()
      ]);
      setProjects(projectsData);
      if (summaryData) setSummary(summaryData);
    } catch (err) {
      console.error('Failed to fetch data', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSync = async () => {
    setSyncing(true);
    try {
      await projectService.triggerSync();
      await fetchData();
    } catch (err) {
      console.error('Sync failed', err);
    } finally {
      setSyncing(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this project?')) {
      const success = await projectService.delete(id);
      if (success) fetchData();
    }
  };

  if (loading) {
    return (
      <Layout title="">
        <div style={{ color: 'var(--text-primary, white)', padding: '24px' }}>Loading dashboard...</div>
      </Layout>
    );
  }

  return (
    <Layout title="Portfolio">
      <div className="portfolio-container">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon"><Activity size={20} color="#0070f3" /></div>
            <div className="stat-info">
              <span className="stat-label">Total Projects</span>
              <span className="stat-value">{projects.length}</span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon"><DollarSign size={20} color="#00c853" /></div>
            <div className="stat-info">
              <span className="stat-label">Total MRR</span>
              <span className="stat-value">
                {summary.total_mrr.toLocaleString('en-US', { style: 'currency', currency: 'USD' })}
              </span>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon"><Users size={20} color="#ffab00" /></div>
            <div className="stat-info">
              <span className="stat-label">Today's Revenue</span>
              <span className="stat-value">
                {summary.total_revenue_today.toLocaleString('en-US', { style: 'currency', currency: 'USD' })}
              </span>
            </div>
          </div>
        </div>

        <div className="section-header">
          <h2>My Projects</h2>
          <div className="header-buttons">
            <button
              className="sync-btn"
              onClick={handleSync}
              disabled={syncing}
            >
              <Activity size={18} className={syncing ? 'spinning' : ''} />
              <span>{syncing ? 'Syncing...' : 'Sync Now'}</span>
            </button>
            <button className="add-project-btn" onClick={() => setIsModalOpen(true)}>
              <Plus size={18} />
              <span>Add Project</span>
            </button>
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading projects...</div>
        ) : projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects registered yet.</p>
            <button className="btn-link" onClick={() => setIsModalOpen(true)}>Add your first project</button>
          </div>
        ) : (
          <div className="project-grid">
            {projects.map((project) => (
              <div key={project.id} className="project-card fade-in">
                <div className="project-header">
                  <div className="project-icon">
                    {project.name.charAt(0).toUpperCase()}
                  </div>
                  <div className="project-meta">
                    <span className="project-type">{project.type}</span>
                    <h3>{project.name}</h3>
                  </div>
                  <div className="project-actions">
                    <button className="action-btn delete" onClick={() => handleDelete(project.id)}>
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                <div className="project-details">
                  <div className="detail-item">
                    <span className="detail-label">Status</span>
                    <span className={`status-pill ${project.status}`}>{project.status}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Provider</span>
                    <span>{project.payment_provider}</span>
                  </div>
                </div>

                <div className="project-footer">
                  {project.api_base_url && (
                    <a href={project.api_base_url} target="_blank" rel="noreferrer" className="visit-link">
                      <ExternalLink size={14} />
                      <span>Visit Site</span>
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <AddProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={fetchData}
      />

      <style>{`
        .portfolio-container {
          display: flex;
          flex-direction: column;
          gap: 40px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 24px;
        }

        .stat-card {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 24px;
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .stat-icon {
          width: 44px;
          height: 44px;
          border-radius: 10px;
          background: rgba(255, 255, 255, 0.03);
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .stat-info {
          display: flex;
          flex-direction: column;
        }

        .stat-label {
          font-size: 0.85rem;
          color: var(--text-secondary);
        }

        .stat-value {
          font-size: 1.25rem;
          font-weight: 700;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-buttons {
          display: flex;
          gap: 12px;
        }

        .sync-btn {
          background: rgba(255, 255, 255, 0.05);
          color: var(--text-primary);
          border: 1px solid var(--border);
          padding: 10px 18px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .sync-btn:hover:not(:disabled) {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--border-hover);
        }

        .sync-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .add-project-btn {
          background: var(--accent);
          color: white;
          border: none;
          padding: 10px 18px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s;
        }

        .add-project-btn:hover {
          transform: translateY(-1px);
        }

        .spinning {
          animation: spinning 1s linear infinite;
        }

        @keyframes spinning {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .project-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 24px;
        }

        .project-card {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 20px;
          transition: border-color 0.2s;
        }

        .project-card:hover {
          border-color: var(--border-hover);
        }

        .project-header {
          display: flex;
          align-items: flex-start;
          gap: 16px;
        }

        .project-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          background: var(--accent-gradient);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 1.2rem;
        }

        .project-meta {
          flex: 1;
        }

        .project-type {
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--text-secondary);
        }

        .project-meta h3 {
          font-size: 1.1rem;
          margin-top: 2px;
        }

        .action-btn {
          background: transparent;
          border: none;
          color: var(--text-secondary);
          cursor: pointer;
          padding: 6px;
          border-radius: 6px;
        }

        .action-btn.delete:hover {
          background: rgba(255, 68, 68, 0.1);
          color: #ff4444;
        }

        .project-details {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .detail-item {
          display: flex;
          justify-content: space-between;
          font-size: 0.9rem;
        }

        .detail-label {
          color: var(--text-secondary);
        }

        .status-pill {
          padding: 2px 10px;
          border-radius: 99px;
          font-size: 0.75rem;
          text-transform: capitalize;
        }

        .status-pill.active {
          background: rgba(0, 200, 83, 0.1);
          color: #00c853;
        }

        .project-footer {
          padding-top: 16px;
          border-top: 1px solid var(--border);
        }

        .visit-link {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 0.85rem;
          color: var(--accent);
          text-decoration: none;
        }

        .empty-state {
          text-align: center;
          padding: 80px;
          background: var(--glass);
          border: 1px dashed var(--border);
          border-radius: 16px;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 16px;
        }

        .btn-link {
          background: none;
          border: none;
          color: var(--accent);
          font-weight: 600;
          cursor: pointer;
          text-decoration: underline;
        }
      `}</style>
    </Layout>
  );
};
