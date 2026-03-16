import React, { useEffect, useState } from 'react';
import {
    Activity,
    Rocket,
    Clock,
    GitBranch,
    CheckCircle2,
    XCircle,
    AlertCircle,
    Play,
    History,
    Terminal,
    Server
} from 'lucide-react';
import { Layout } from '../../components/Layout';
import { deploymentService } from '../../services/deploymentService';
import type { Deployment } from '../../services/deploymentService';
import { projectService } from '../../services/projectService';

const Deployments: React.FC = () => {
    const [deployments, setDeployments] = useState<Deployment[]>([]);
    const [projects, setProjects] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [isDeploying, setIsDeploying] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [deployList, projectList] = await Promise.all([
                    deploymentService.getDeployments(),
                    projectService.getAll()
                ]);
                setDeployments(deployList);
                setProjects(projectList);
            } catch (err) {
                console.error('Failed to fetch deployment data', err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();

        // Polling for updates every 10 seconds (could be WebSockets later)
        const interval = setInterval(async () => {
            const list = await deploymentService.getDeployments();
            setDeployments(list);
        }, 10000);

        return () => clearInterval(interval);
    }, []);

    const handleTriggerDeploy = async (projectId: string, env: 'development' | 'staging' | 'production') => {
        setIsDeploying(true);
        const result = await deploymentService.triggerDeployment(projectId, env);
        if (result) {
            setDeployments([result, ...deployments]);
        }
        setIsDeploying(false);
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'deployed': return <CheckCircle2 size={16} color="#00c853" />;
            case 'building': return <Activity size={16} className="spin" color="#ffd600" />;
            case 'failed': return <XCircle size={16} color="#ff4444" />;
            case 'queued': return <Clock size={16} color="#94a3b8" />;
            default: return <AlertCircle size={16} color="#94a3b8" />;
        }
    };

    const getEnvClass = (env: string) => {
        switch (env) {
            case 'production': return 'env-prod';
            case 'staging': return 'env-staging';
            default: return 'env-dev';
        }
    };

    if (loading) {
        return (
            <Layout title="Deployments">
                <div style={{ display: 'flex', justifyContent: 'center', padding: '100px', color: 'var(--text-secondary)' }}>
                    Loading monitoring dashboard...
                </div>
            </Layout>
        );
    }

    return (
        <Layout title="Deployments">
            <div className="deployments-wrapper fade-in">
                {/* Stats Header */}
                <div className="stats-row">
                    <div className="stat-card">
                        <Rocket size={20} color="#0070f3" />
                        <div className="stat-info">
                            <span className="label">Total Deploys</span>
                            <span className="value">{deployments.length}</span>
                        </div>
                    </div>
                    <div className="stat-card">
                        <Activity size={20} color="#00c853" />
                        <div className="stat-info">
                            <span className="label">Success Rate</span>
                            <span className="value">98.2%</span>
                        </div>
                    </div>
                    <div className="stat-card">
                        <Terminal size={20} color="#94a3b8" />
                        <div className="stat-info">
                            <span className="label">Active Pipelines</span>
                            <span className="value">{deployments.filter(d => d.status === 'building').length}</span>
                        </div>
                    </div>
                </div>

                <div className="dashboard-grid">
                    {/* Active Monitoring Table */}
                    <div className="main-panel card">
                        <div className="card-header">
                            <div className="title">
                                <History size={20} />
                                <h2>Recent Activity</h2>
                            </div>
                            <button className="btn-refresh" onClick={() => window.location.reload()}>
                                <Activity size={14} /> Refresh
                            </button>
                        </div>

                        <div className="table-container">
                            <table className="custom-table">
                                <thead>
                                    <tr>
                                        <th>Project</th>
                                        <th>Environment</th>
                                        <th>Status</th>
                                        <th>Version</th>
                                        <th>Commit</th>
                                        <th>Date</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {deployments.map((dep) => (
                                        <tr key={dep.id}>
                                            <td className="bold">{projects.find(p => p.id === dep.project_id)?.name || 'Project'}</td>
                                            <td>
                                                <span className={`badge ${getEnvClass(dep.environment)}`}>
                                                    {dep.environment.toUpperCase()}
                                                </span>
                                            </td>
                                            <td>
                                                <div className="status-cell">
                                                    {getStatusIcon(dep.status)}
                                                    <span className={`status-text status-${dep.status}`}>{dep.status}</span>
                                                </div>
                                            </td>
                                            <td className="mono">{dep.version || '1.0.0'}</td>
                                            <td className="mono commit">
                                                <GitBranch size={12} /> {dep.commit_hash?.substring(0, 7) || '---'}
                                            </td>
                                            <td className="text-secondary">{new Date(dep.deployed_at).toLocaleString()}</td>
                                            <td>
                                                <button className="icon-btn" title="View Logs"><Terminal size={14} /></button>
                                            </td>
                                        </tr>
                                    ))}
                                    {deployments.length === 0 && (
                                        <tr>
                                            <td colSpan={7} className="empty-state">No deployments found.</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* Quick Actions Panel */}
                    <div className="side-panel">
                        <div className="card">
                            <div className="card-header">
                                <div className="title">
                                    <Play size={20} />
                                    <h2>Trigger Deploy</h2>
                                </div>
                            </div>
                            <div className="actions-list">
                                {projects.map(project => (
                                    <div key={project.id} className="project-action-card">
                                        <div className="proj-info">
                                            <span className="proj-name">{project.name}</span>
                                            <span className="proj-type">{project.type}</span>
                                        </div>
                                        <div className="btn-group">
                                            <button
                                                className="btn-deploy btn-staging"
                                                disabled={isDeploying}
                                                onClick={() => handleTriggerDeploy(project.id, 'staging')}
                                            >
                                                Staging
                                            </button>
                                            <button
                                                className="btn-deploy btn-prod"
                                                disabled={isDeploying}
                                                onClick={() => handleTriggerDeploy(project.id, 'production')}
                                            >
                                                Production
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="card terminal-preview">
                            <div className="card-header">
                                <span className="title"><Server size={18} /> System Status</span>
                            </div>
                            <div className="sys-status">
                                <div className="sys-item">
                                    <span>Main Cluster</span>
                                    <span className="status-dot online"></span>
                                </div>
                                <div className="sys-item">
                                    <span>API Gateway</span>
                                    <span className="status-dot online"></span>
                                </div>
                                <div className="sys-item">
                                    <span>CI-CD Worker</span>
                                    <span className="status-dot warning"></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <style>{`
                .deployments-wrapper {
                    display: flex;
                    flex-direction: column;
                    gap: 24px;
                }
                .stats-row {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                }
                .stat-card {
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    padding: 24px;
                    border-radius: 16px;
                    display: flex;
                    align-items: center;
                    gap: 16px;
                    transition: transform 0.2s;
                }
                .stat-card:hover { transform: translateY(-4px); }
                .stat-info .label { font-size: 0.8rem; color: var(--text-secondary); display: block; }
                .stat-info .value { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }

                .dashboard-grid {
                    display: grid;
                    grid-template-columns: 1fr 340px;
                    gap: 24px;
                }
                .card {
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-radius: 16px;
                    overflow: hidden;
                }
                .card-header {
                    padding: 20px 24px;
                    border-bottom: 1px solid var(--border);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .card-header .title { display: flex; align-items: center; gap: 12px; }
                .card-header h2 { font-size: 1.1rem; font-weight: 600; margin: 0; }
                
                .table-container { padding: 8px; }
                .custom-table { width: 100%; border-collapse: collapse; text-align: left; }
                .custom-table th { padding: 16px; font-size: 0.8rem; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 0.05em; }
                .custom-table td { padding: 16px; border-top: 1px solid var(--border); font-size: 0.9rem; }
                .custom-table tr:hover { background: rgba(255, 255, 255, 0.02); }
                
                .bold { font-weight: 600; color: var(--text-primary); }
                .mono { font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 0.8rem; opacity: 0.8; }
                .commit { display: flex; align-items: center; gap: 4px; color: var(--accent); }
                
                .badge { padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
                .env-prod { background: rgba(147, 51, 234, 0.1); color: #a855f7; border: 1px solid rgba(147, 51, 234, 0.2); }
                .env-staging { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
                .env-dev { background: rgba(59, 130, 246, 0.1); color: #3b82f6; border: 1px solid rgba(59, 130, 246, 0.2); }
                
                .status-cell { display: flex; align-items: center; gap: 8px; }
                .status-text { text-transform: capitalize; font-size: 0.85rem; font-weight: 500; }
                .status-deployed { color: #00c853; }
                .status-building { color: #ffd600; }
                .status-failed { color: #ff4444; }

                .side-panel { display: flex; flex-direction: column; gap: 24px; }
                .project-action-card { padding: 16px 20px; border-bottom: 1px solid var(--border); }
                .proj-info { margin-bottom: 12px; display: flex; flex-direction: column; }
                .proj-name { font-weight: 600; color: var(--text-primary); }
                .proj-type { font-size: 0.75rem; color: var(--text-secondary); }
                
                .btn-group { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
                .btn-deploy { padding: 8px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; cursor: pointer; border: 1px solid var(--border); transition: all 0.2s; }
                .btn-staging { background: rgba(245, 158, 11, 0.05); color: #f59e0b; }
                .btn-staging:hover { background: #f59e0b; color: #fff; }
                .btn-prod { background: rgba(147, 51, 234, 0.05); color: #a855f7; }
                .btn-prod:hover { background: #a855f7; color: #fff; }
                .btn-deploy:disabled { opacity: 0.5; cursor: not-allowed; }

                .sys-status { padding: 20px 24px; display: flex; flex-direction: column; gap: 12px; }
                .sys-item { display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }
                .status-dot { width: 8px; height: 8px; border-radius: 50%; }
                .online { background: #00c853; box-shadow: 0 0 10px rgba(0, 200, 83, 0.5); }
                .warning { background: #ffd600; box-shadow: 0 0 10px rgba(255, 214, 0, 0.5); }

                @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                .spin { animation: spin 2s linear infinite; }
            `}</style>
        </Layout>
    );
};

export default Deployments;
