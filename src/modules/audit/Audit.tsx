import React, { useEffect, useState } from 'react';
import { Shield, Search, Download, AlertCircle } from 'lucide-react';
import { auditService } from '../../services/auditService';
import type { AuditLog } from '../../services/auditService';
import { Layout } from '../../components/Layout';

export const Audit: React.FC = () => {
    const [logs, setLogs] = useState<AuditLog[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchLogs = async () => {
            setLoading(true);
            try {
                const data = await auditService.getLogs();
                setLogs(data);
            } catch (err) {
                console.error('Failed to fetch audit logs', err);
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, []);

    const filteredLogs = logs.filter(log =>
        log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (log.entity && log.entity.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    if (loading) {
        return (
            <Layout title="Security">
                <div style={{ color: 'var(--text-primary, white)', padding: '24px' }}>Accessing security logs...</div>
            </Layout>
        );
    }

    return (
        <Layout title="Security">
            <div className="audit-container fade-in">

                {/* Stats / Overview row (optional, matching previous style) */}
                <div className="stats-grid" style={{ marginBottom: '24px' }}>
                    <div className="stat-card">
                        <div className="stat-icon"><Shield size={24} color="#0070f3" /></div>
                        <div className="stat-info">
                            <span className="stat-label">Total Audit Events</span>
                            <div className="stat-value-group">
                                <span className="stat-value">{logs.length}</span>
                            </div>
                        </div>
                    </div>
                    <div className="stat-card" style={{ flex: '2 1 400px', maxWidth: '100%' }}>
                        <div className="stat-info" style={{ width: '100%', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div>
                                <span className="stat-label">System Status</span>
                                <div className="stat-value-group" style={{ marginTop: '8px' }}>
                                    <AlertCircle size={20} color="#00c853" />
                                    <span style={{ color: '#00c853', fontWeight: 600 }}>All Systems Secure</span>
                                </div>
                            </div>
                            <div className="search-box">
                                <Search size={18} color="var(--text-secondary)" />
                                <input
                                    type="text"
                                    placeholder="Search by action or entity..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="dashboard-content">
                    <div className="section-header">
                        <h2>Audit & Security Logs</h2>
                        <div className="header-actions">
                            <button className="btn-secondary">
                                <Download size={16} /> Export Logs
                            </button>
                            <button className="btn-primary">Manage Access</button>
                        </div>
                    </div>

                    <div className="logs-table-wrapper">
                        {filteredLogs.length === 0 ? (
                            <div className="empty-state">
                                <h3>No matching logs found.</h3>
                                <p>System changes, access attempts, and project modifications will be recorded here.</p>
                                <button className="btn-link">View documentation on audit logs</button>
                            </div>
                        ) : (
                            <div className="table-container">
                                <table className="data-table">
                                    <thead>
                                        <tr>
                                            <th>Timestamp</th>
                                            <th>Action</th>
                                            <th>Entity</th>
                                            <th>ID</th>
                                            <th>IP Address</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {filteredLogs.map(log => (
                                            <tr key={log.id}>
                                                <td className="timestamp-cell">
                                                    {new Date(log.timestamp).toLocaleString(undefined, {
                                                        year: 'numeric', month: 'short', day: 'numeric',
                                                        hour: '2-digit', minute: '2-digit'
                                                    })}
                                                </td>
                                                <td>
                                                    <span className={`action-pill ${log.action.toLowerCase().replace(/\s+/g, '_')}`}>
                                                        {log.action}
                                                    </span>
                                                </td>
                                                <td><strong>{log.entity || '-'}</strong></td>
                                                <td><code>{log.entity_id || '-'}</code></td>
                                                <td className="ip-cell">{log.ip_address || 'Internal'}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </div>

                <style>{`
                    .audit-container {
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

                    .search-box {
                        display: flex;
                        align-items: center;
                        gap: 10px;
                        background: rgba(255, 255, 255, 0.05);
                        border: 1px solid var(--border);
                        border-radius: 8px;
                        padding: 10px 16px;
                        width: 320px;
                        transition: border-color 0.2s;
                    }

                    .search-box:focus-within {
                        border-color: #0070f3;
                    }

                    .search-box input {
                        background: none;
                        border: none;
                        color: white;
                        font-size: 0.95rem;
                        width: 100%;
                        outline: none;
                    }

                    .search-box input::placeholder {
                        color: var(--text-secondary);
                    }

                    .dashboard-content {
                        margin-top: 8px;
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
                        max-width: 480px;
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

                    .timestamp-cell {
                        color: var(--text-secondary) !important;
                        font-size: 0.85rem !important;
                    }

                    .ip-cell {
                        font-family: monospace;
                        color: var(--text-secondary) !important;
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

                    .action-pill {
                        padding: 4px 10px;
                        border-radius: 20px;
                        font-size: 0.8rem;
                        font-weight: 500;
                        text-transform: capitalize;
                        display: inline-block;
                        background: rgba(0, 112, 243, 0.15);
                        color: #0070f3;
                    }
                    
                    /* Dynamic action colors */
                    .action-pill.delete, .action-pill.remove, .action-pill.delete_project {
                        background: rgba(255, 82, 82, 0.15) !important;
                        color: #ff5252 !important;
                    }

                    .action-pill.create, .action-pill.add, .action-pill.create_project {
                        background: rgba(0, 200, 83, 0.15) !important;
                        color: #00c853 !important;
                    }

                    .action-pill.update, .action-pill.edit {
                        background: rgba(255, 171, 0, 0.15) !important;
                        color: #ffab00 !important;
                    }
                `}</style>
            </div>
        </Layout>
    );
};
