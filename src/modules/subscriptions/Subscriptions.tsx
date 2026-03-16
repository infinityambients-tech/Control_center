import React, { useEffect, useState } from 'react';
import { Users, Clock, AlertTriangle, Download } from 'lucide-react';
import { subscriptionService } from '../../services/subscriptionService';
import type { SubscriptionSummary, SubscriptionSnapshot } from '../../services/subscriptionService';
import { Layout } from '../../components/Layout';

const Subscriptions: React.FC = () => {
    const [summary, setSummary] = useState<SubscriptionSummary | null>(null);
    const [subscriptions, setSubscriptions] = useState<SubscriptionSnapshot[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [s, subList] = await Promise.all([
                    subscriptionService.getSummary(),
                    subscriptionService.getAll(50)
                ]);
                setSummary(s);
                setSubscriptions(subList);
            } catch (err) {
                console.error('Subscription data load failed', err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <Layout title="Subscriptions">
                <div style={{ color: 'var(--text-primary, white)', padding: '24px' }}>Loading subscription metrics...</div>
            </Layout>
        );
    }

    return (
        <Layout title="Subscriptions">
            <div className="subscriptions-container fade-in">
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-icon"><Users size={24} color="#0070f3" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Active Users</span>
                            <div className="stat-value-group">
                                <span className="stat-value">{summary?.total_active?.toLocaleString() || '0'}</span>
                            </div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon"><Clock size={24} color="#ffab00" /></div>
                        <div className="stat-info" style={{ width: '100%' }}>
                            <span className="stat-label">Plan Distribution</span>
                            <div className="plan-dist">
                                {summary?.plans_distribution && Object.entries(summary.plans_distribution).map(([plan, count]) => (
                                    <div key={plan} className="plan-item">
                                        <span className="plan-name">{plan}</span>
                                        <span className="plan-count">{count}</span>
                                    </div>
                                ))}
                                {!summary?.plans_distribution && (
                                    <div className="plan-item">
                                        <span className="plan-name">No data</span>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon"><AlertTriangle size={24} color="#ff5252" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Churned (Total)</span>
                            <div className="stat-value-group">
                                <span className="stat-value">{summary?.churned_count || '0'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content">
                    <div className="section-header">
                        <h2>Recent Subscription Actions</h2>
                        <div className="header-actions">
                            <button className="btn-secondary">
                                <Download size={16} /> Export CSV
                            </button>
                            <button className="btn-primary">Manage</button>
                        </div>
                    </div>
                    <div className="subs-list">
                        {subscriptions.length === 0 ? (
                            <div className="empty-state">
                                <h3>No subscription data found.</h3>
                                <p>Once users subscribe to your plans, their active status and renewal dates will appear here.</p>
                                <button className="btn-link">View documentation on subscriptions</button>
                            </div>
                        ) : (
                            <div className="table-container">
                                <table className="data-table">
                                    <thead>
                                        <tr>
                                            <th>Status</th>
                                            <th>Plan</th>
                                            <th>External ID</th>
                                            <th>Renews/Ends</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {subscriptions.map(sub => (
                                            <tr key={sub.id}>
                                                <td><span className={`status-pill ${sub.status}`}>{sub.status}</span></td>
                                                <td><strong>{sub.plan}</strong></td>
                                                <td><code>{sub.external_id}</code></td>
                                                <td>{new Date(sub.current_period_end).toLocaleDateString()}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>

                <style>{`
                    .subscriptions-container {
                        display: flex;
                        flex-direction: column;
                        gap: 24px;
                    }

                    .stats-grid {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 24px;
                    }

                    .stat-card {
                        background: rgba(255, 255, 255, 0.03);
                        border: 1px solid var(--border);
                        border-radius: 12px;
                        padding: 24px;
                        display: flex;
                        align-items: center;
                        gap: 20px;
                        flex: 1 1 300px;
                        max-width: 380px;
                    }

                    .stat-icon {
                        background: rgba(255, 255, 255, 0.04);
                        border-radius: 12px;
                        padding: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }

                    .stat-info {
                        display: flex;
                        flex-direction: column;
                        gap: 4px;
                    }

                    .stat-label {
                        color: var(--text-secondary);
                        font-size: 0.95rem;
                        font-weight: 500;
                    }

                    .stat-value-group {
                        display: flex;
                        align-items: baseline;
                        gap: 12px;
                        margin-top: 4px;
                    }

                    .stat-value {
                        color: var(--text-primary);
                        font-size: 1.8rem;
                        font-weight: 700;
                        letter-spacing: -0.02em;
                    }

                    /* Custom for Plan Distribution */
                    .plan-dist {
                        display: flex;
                        flex-direction: column;
                        gap: 8px;
                        margin-top: 12px;
                        width: 100%;
                    }
                    .plan-item {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        font-size: 0.9rem;
                        background: rgba(255, 255, 255, 0.02);
                        padding: 6px 10px;
                        border-radius: 6px;
                    }
                    .plan-name {
                        color: var(--text-primary);
                        font-weight: 500;
                    }
                    .plan-count {
                        color: #ffab00;
                        font-weight: 700;
                        background: rgba(255, 171, 0, 0.1);
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 0.85rem;
                    }

                    .dashboard-content {
                        margin-top: 16px;
                    }

                    .section-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 24px;
                    }

                    .section-header h2 {
                        font-size: 1.5rem;
                        font-weight: 700;
                        color: white;
                    }

                    .header-actions {
                        display: flex;
                        gap: 12px;
                    }

                    .btn-primary {
                        background: #0070f3;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-size: 0.9rem;
                        font-weight: 600;
                        cursor: pointer;
                        transition: background 0.2s;
                    }

                    .btn-primary:hover {
                        background: #0060df;
                    }

                    .btn-secondary {
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid var(--border);
                        color: white;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-size: 0.9rem;
                        font-weight: 500;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        transition: all 0.2s;
                    }

                    .btn-secondary:hover {
                        background: rgba(255, 255, 255, 0.1);
                    }

                    .empty-state {
                        background: rgba(255, 255, 255, 0.02);
                        border: 1px dashed var(--border);
                        border-radius: 12px;
                        padding: 60px 24px;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        gap: 12px;
                    }

                    .empty-state h3 {
                        font-size: 1.1rem;
                        color: var(--text-primary);
                        font-weight: 500;
                    }

                    .empty-state p {
                        color: var(--text-secondary);
                        font-size: 0.95rem;
                        max-width: 400px;
                    }

                    .btn-link {
                        background: none;
                        border: none;
                        color: #0070f3;
                        font-size: 0.95rem;
                        font-weight: 500;
                        cursor: pointer;
                        margin-top: 8px;
                    }

                    .btn-link:hover {
                        text-decoration: underline;
                    }

                    .table-container {
                        background: rgba(255, 255, 255, 0.02);
                        border: 1px solid var(--border);
                        border-radius: 12px;
                        overflow: hidden;
                    }

                    .data-table {
                        width: 100%;
                        border-collapse: collapse;
                    }

                    .data-table th {
                        text-align: left;
                        color: var(--text-secondary);
                        font-size: 0.85rem;
                        font-weight: 500;
                        padding: 16px 24px;
                        border-bottom: 1px solid var(--border);
                        background: rgba(255, 255, 255, 0.01);
                    }

                    .data-table td {
                        padding: 16px 24px;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                        color: var(--text-primary);
                        font-size: 0.95rem;
                    }
                    
                    .data-table tr:last-child td {
                        border-bottom: none;
                    }

                    code {
                        background: rgba(255, 255, 255, 0.05);
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-family: monospace;
                        font-size: 0.85rem;
                        color: var(--text-secondary);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }

                    .status-pill {
                        padding: 4px 10px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 500;
                        text-transform: capitalize;
                    }

                    .status-pill.active {
                        background: rgba(0, 200, 83, 0.15);
                        color: #00c853;
                    }

                    .status-pill.canceled {
                        background: rgba(255, 82, 82, 0.15);
                        color: #ff5252;
                    }
                    
                    .status-pill.past_due {
                        background: rgba(255, 171, 0, 0.15);
                        color: #ffab00;
                    }
                `}</style>
            </div>
        </Layout>
    );
};

export default Subscriptions;
