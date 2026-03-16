import React, { useEffect, useState } from 'react';
import { Layers, Shield, Users, Database, Check, Zap } from 'lucide-react';
import { planService } from '../../services/planService';
import type { Plan } from '../../services/planService';
import { Layout } from '../../components/Layout';

const Plans: React.FC = () => {
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPlans = async () => {
            setLoading(true);
            try {
                const data = await planService.getPlans();
                setPlans(data);
            } catch (err) {
                console.error('Failed to fetch plans', err);
            } finally {
                setLoading(false);
            }
        };
        fetchPlans();
    }, []);

    if (loading) {
        return (
            <Layout title="Plans & Limits">
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>Loading plans and infrastructure limits...</p>
                </div>
                <style>{`
                    .loading-container {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 60vh;
                        color: var(--text-secondary);
                        gap: 16px;
                    }
                    .loading-spinner {
                        width: 40px;
                        height: 40px;
                        border: 3px solid rgba(0, 112, 243, 0.1);
                        border-top-color: var(--accent);
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    }
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                `}</style>
            </Layout>
        );
    }

    return (
        <Layout title="Plans & Limits">
            <div className="plans-container fade-in">
                <div className="plans-header">
                    <div className="header-info">
                        <h1>Subscription Plans</h1>
                        <p>Scale your infrastructure with our flexible tiers tailored for your company size.</p>
                    </div>
                    <button className="btn-primary">
                        <Zap size={18} /> Upgrade Plan
                    </button>
                </div>

                <div className="plans-grid">
                    {plans.map((plan) => (
                        <div key={plan.id} className={`plan-card ${plan.name.toLowerCase() === 'pro' ? 'featured' : ''}`}>
                            {plan.name.toLowerCase() === 'pro' && <div className="featured-badge">Most Popular</div>}
                            <div className="plan-name">{plan.name}</div>
                            <div className="plan-price-block">
                                <span className="currency">$</span>
                                <span className="price">{plan.monthly_price}</span>
                                <span className="period">/month</span>
                            </div>

                            <div className="plan-limits">
                                <div className="limit-item">
                                    <Layers size={18} />
                                    <span><strong>{plan.max_projects}</strong> Projects</span>
                                </div>
                                <div className="limit-item">
                                    <Users size={18} />
                                    <span><strong>{plan.max_users}</strong> Team Members</span>
                                </div>
                                <div className="limit-item">
                                    <Database size={18} />
                                    <span><strong>{plan.max_storage_gb}GB</strong> Storage</span>
                                </div>
                                <div className="limit-item">
                                    <Shield size={18} />
                                    <span>{plan.priority_support ? 'Priority Support' : 'Standard Support'}</span>
                                </div>
                            </div>

                            <div className="plan-features">
                                <div className="feature">
                                    <Check size={16} />
                                    <span>Real-time Analytics</span>
                                </div>
                                <div className="feature">
                                    <Check size={16} />
                                    <span>Deployment Monitor</span>
                                </div>
                                <div className="feature">
                                    <Check size={16} />
                                    <span>Invoicing System</span>
                                </div>
                            </div>

                            <button className={`plan-btn ${plan.name.toLowerCase() === 'pro' ? 'btn-primary' : 'btn-secondary'}`}>
                                Select {plan.name}
                            </button>
                        </div>
                    ))}

                    {/* Placeholder Plans if none exist in DB yet */}
                    {plans.length === 0 && (
                        <>
                            <div className="plan-card">
                                <div className="plan-name">Free Tier</div>
                                <div className="plan-price-block">
                                    <span className="currency">$</span>
                                    <span className="price">0</span>
                                    <span className="period">/month</span>
                                </div>
                                <div className="plan-limits">
                                    <div className="limit-item"><Layers size={18} /><span><strong>1</strong> Project</span></div>
                                    <div className="limit-item"><Users size={18} /><span><strong>1</strong> User</span></div>
                                    <div className="limit-item"><Database size={18} /><span><strong>1GB</strong> Storage</span></div>
                                </div>
                                <button className="plan-btn btn-secondary disabled" disabled>Currently Active</button>
                            </div>
                            <div className="plan-card featured">
                                <div className="featured-badge">Recommended</div>
                                <div className="plan-name">Professional</div>
                                <div className="plan-price-block">
                                    <span className="currency">$</span>
                                    <span className="price">49</span>
                                    <span className="period">/month</span>
                                </div>
                                <div className="plan-limits">
                                    <div className="limit-item"><Layers size={18} /><span><strong>10</strong> Projects</span></div>
                                    <div className="limit-item"><Users size={18} /><span><strong>5</strong> Users</span></div>
                                    <div className="limit-item"><Database size={18} /><span><strong>20GB</strong> Storage</span></div>
                                    <div className="limit-item"><Shield size={18} /><span>Priority Support</span></div>
                                </div>
                                <button className="plan-btn btn-primary">Upgrade Now</button>
                            </div>
                        </>
                    )}
                </div>
            </div>

            <style>{`
                .plans-container {
                    padding: 8px;
                }
                .plans-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-end;
                    margin-bottom: 40px;
                }
                .header-info h1 {
                    font-size: 2rem;
                    font-weight: 800;
                    margin-bottom: 8px;
                    color: var(--text-primary);
                }
                .header-info p {
                    color: var(--text-secondary);
                    font-size: 1.1rem;
                }
                .plans-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
                    gap: 32px;
                }
                .plan-card {
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid var(--border);
                    border-radius: 24px;
                    padding: 40px;
                    display: flex;
                    flex-direction: column;
                    position: relative;
                    transition: all 0.3s ease;
                }
                .plan-card:hover {
                    transform: translateY(-8px);
                    border-color: rgba(0, 112, 243, 0.3);
                    background: rgba(255, 255, 255, 0.05);
                }
                .plan-card.featured {
                    border-color: var(--accent);
                    background: rgba(0, 112, 243, 0.05);
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                }
                .featured-badge {
                    position: absolute;
                    top: -14px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: var(--accent);
                    color: white;
                    padding: 6px 16px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                .plan-name {
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: var(--text-secondary);
                    margin-bottom: 16px;
                }
                .plan-price-block {
                    margin-bottom: 32px;
                    display: flex;
                    align-items: baseline;
                }
                .currency {
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: var(--text-primary);
                    margin-right: 4px;
                }
                .price {
                    font-size: 3.5rem;
                    font-weight: 800;
                    color: var(--text-primary);
                    letter-spacing: -0.02em;
                }
                .period {
                    font-size: 1rem;
                    color: var(--text-secondary);
                    margin-left: 8px;
                }
                .plan-limits {
                    border-top: 1px solid var(--border);
                    border-bottom: 1px solid var(--border);
                    padding: 24px 0;
                    margin-bottom: 24px;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                }
                .limit-item {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    color: var(--text-primary);
                    font-size: 0.95rem;
                }
                .limit-item strong {
                    font-weight: 700;
                }
                .limit-item svg {
                    color: var(--accent);
                }
                .plan-features {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                    margin-bottom: 32px;
                }
                .feature {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    color: var(--text-secondary);
                    font-size: 0.9rem;
                }
                .feature svg {
                    color: #00c853;
                }
                .plan-btn {
                    margin-top: auto;
                    width: 100%;
                    padding: 16px;
                    border-radius: 12px;
                    font-size: 1rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.2s;
                    border: none;
                }
                .btn-primary {
                    background: var(--accent);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                }
                .btn-primary:hover {
                    background: #0060df;
                    box-shadow: 0 8px 20px rgba(0, 112, 243, 0.4);
                }
                .btn-secondary {
                    background: rgba(255, 255, 255, 0.05);
                    color: white;
                    border: 1px solid var(--border);
                }
                .btn-secondary:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                .plan-btn.disabled {
                    background: rgba(255, 255, 255, 0.02);
                    color: var(--text-secondary);
                    border: none;
                    cursor: not-allowed;
                }
            `}</style>
        </Layout>
    );
};

export default Plans;
