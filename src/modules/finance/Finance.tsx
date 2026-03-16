import React, { useEffect, useState } from 'react';
import { DollarSign, TrendingUp, Users, ArrowUpRight, ArrowDownRight, Download } from 'lucide-react';
import { financeService } from '../../services/financeService';
import type { FinanceSummary, PaymentSnapshot } from '../../services/financeService';
import { Layout } from '../../components/Layout';

const Finance: React.FC = () => {
    const [summary, setSummary] = useState<FinanceSummary | null>(null);
    const [payments, setPayments] = useState<PaymentSnapshot[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [s, p] = await Promise.all([
                    financeService.getSummary(),
                    financeService.getRecentPayments(10)
                ]);
                setSummary(s);
                setPayments(p);
            } catch (err) {
                console.error('Finance data load failed', err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <Layout title="Finance">
                <div style={{ color: 'var(--text-primary, white)', padding: '24px' }}>Loading financial data...</div>
            </Layout>
        );
    }

    return (
        <Layout title="Finance">
            <div className="finance-container fade-in">
                <div className="stats-grid">
                    <div className="stat-card">
                        <div className="stat-icon"><DollarSign size={24} color="#00c853" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Total Revenue</span>
                            <div className="stat-value-group">
                                <span className="stat-value">${summary?.total_revenue?.toLocaleString() || '0'}</span>
                            </div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon"><TrendingUp size={24} color="#0070f3" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Total MRR</span>
                            <div className="stat-value-group">
                                <span className="stat-value">${summary?.mrr?.toLocaleString() || '0'}</span>
                                <span className="stat-trend positive">
                                    <ArrowUpRight size={16} /> {summary?.mrr_growth || '0'}%
                                </span>
                            </div>
                        </div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-icon"><Users size={24} color="#ffab00" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Churn Rate</span>
                            <div className="stat-value-group">
                                <span className="stat-value">{summary?.churn_rate || '0'}%</span>
                                <span className="stat-trend negative">
                                    <ArrowDownRight size={16} /> 0.2%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content">
                    <div className="section-header">
                        <h2>Recent Payments</h2>
                        <div className="header-actions">
                            <button className="btn-secondary">
                                <Download size={16} /> Export Report
                            </button>
                            <button className="btn-primary">View All</button>
                        </div>
                    </div>

                    <div className="payments-list">
                        {payments.length === 0 ? (
                            <div className="empty-state">
                                <h3>No payments registered yet.</h3>
                                <p>When you start receiving remote payments, they will automatically sync here.</p>
                                <button className="btn-link">View documentation on integrations</button>
                            </div>
                        ) : (
                            <div className="table-container">
                                <table className="data-table">
                                    <thead>
                                        <tr>
                                            <th>Date</th>
                                            <th>Project</th>
                                            <th>Amount</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {payments.map(pay => (
                                            <tr key={pay.id}>
                                                <td>{new Date(pay.created_at).toLocaleDateString()}</td>
                                                <td>{pay.project_id.split('-')[0]}...</td>
                                                <td className="amount-cell">{pay.amount} {pay.currency}</td>
                                                <td><span className={`status-pill ${pay.status}`}>{pay.status}</span></td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>

                <style>{`
                    .finance-container {
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
                    }

                    .stat-value {
                        color: var(--text-primary);
                        font-size: 1.8rem;
                        font-weight: 700;
                        letter-spacing: -0.02em;
                    }

                    .stat-trend {
                        display: flex;
                        align-items: center;
                        gap: 2px;
                        font-size: 0.85rem;
                        font-weight: 600;
                    }
                    
                    .stat-trend.positive { color: #00c853; }
                    .stat-trend.negative { color: #ff5252; }
                    
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

                    .amount-cell {
                        font-family: monospace;
                        font-size: 1.05rem !important;
                    }

                    .status-pill {
                        padding: 4px 10px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 500;
                        text-transform: capitalize;
                    }

                    .status-pill.completed {
                        background: rgba(0, 200, 83, 0.15);
                        color: #00c853;
                    }

                    .status-pill.pending {
                        background: rgba(255, 171, 0, 0.15);
                        color: #ffab00;
                    }

                    .status-pill.failed {
                        background: rgba(255, 82, 82, 0.15);
                        color: #ff5252;
                    }
                `}</style>
            </div>
        </Layout>
    );
};

export default Finance;
