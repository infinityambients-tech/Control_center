import React, { useState } from 'react';
import { X, Globe, Tag, CreditCard, Activity } from 'lucide-react';
import { projectService } from '../../services/projectService';

interface AddProjectModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export const AddProjectModal: React.FC<AddProjectModalProps> = ({ isOpen, onClose, onSuccess }) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        type: 'SaaS',
        api_base_url: '',
        api_key: '',
        payment_provider: 'PayPal',
    });

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const success = await projectService.add(formData);
            if (success) {
                onSuccess();
                onClose();
            }
        } catch (err) {
            console.error('Failed to add project', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content fade-in" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Add New Project</h2>
                    <button className="close-button" onClick={onClose}>
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label><Tag size={16} /> Project Name</label>
                        <input
                            required
                            type="text"
                            placeholder="My Awesome SaaS"
                            value={formData.name}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label><Activity size={16} /> Type</label>
                            <select
                                value={formData.type}
                                onChange={e => setFormData({ ...formData, type: e.target.value })}
                            >
                                <option>SaaS</option>
                                <option>E-commerce</option>
                                <option>Service</option>
                                <option>Open Source</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label><CreditCard size={16} /> Payment Provider</label>
                            <select
                                value={formData.payment_provider}
                                onChange={e => setFormData({ ...formData, payment_provider: e.target.value })}
                            >
                                <option>PayPal</option>
                                <option>Stripe</option>
                                <option>LemonSqueezy</option>
                                <option>None</option>
                            </select>
                        </div>
                    </div>

                    <div className="form-group">
                        <label><Globe size={16} /> API Base URL</label>
                        <input
                            type="url"
                            placeholder="https://api.myproject.com"
                            value={formData.api_base_url}
                            onChange={e => setFormData({ ...formData, api_base_url: e.target.value })}
                        />
                    </div>

                    <div className="form-group">
                        <label><Activity size={16} /> API Key (Admin Sync)</label>
                        <input
                            type="password"
                            placeholder="Paste your API key here"
                            value={formData.api_key}
                            onChange={e => setFormData({ ...formData, api_key: e.target.value })}
                        />
                        <p className="form-help">This key will be encrypted and used for metrics synchronization.</p>
                    </div>

                    <div className="modal-footer">
                        <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? 'Adding...' : 'Add Project'}
                        </button>
                    </div>
                </form>
            </div>

            <style>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.8);
          backdrop-filter: blur(4px);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }

        .modal-content {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: 16px;
          width: 500px;
          max-width: 90vw;
          padding: 32px;
          position: relative;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }

        .close-button {
          background: transparent;
          border: none;
          color: var(--text-secondary);
          cursor: pointer;
          padding: 4px;
        }

        .form-group {
          margin-bottom: 20px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .form-group label {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 0.9rem;
          color: var(--text-secondary);
        }

        .form-help {
          font-size: 0.75rem;
          color: var(--text-secondary);
          opacity: 0.7;
          margin-top: 4px;
        }

        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }

        input, select {
          background: var(--bg-dark);
          border: 1px solid var(--border);
          border-radius: 8px;
          padding: 12px;
          color: var(--text-primary);
          font-size: 1rem;
          width: 100%;
        }

        input:focus {
          outline: none;
          border-color: var(--accent);
        }

        .modal-footer {
          margin-top: 32px;
          display: flex;
          justify-content: flex-end;
          gap: 12px;
        }

        .btn-primary {
          background: var(--accent);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
        }

        .btn-secondary {
          background: transparent;
          color: var(--text-secondary);
          border: 1px solid var(--border);
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
        }
      `}</style>
        </div>
    );
};
