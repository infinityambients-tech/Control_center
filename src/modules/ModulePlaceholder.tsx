import React from 'react';
import { Layout } from '../components/Layout';
import { Construction } from 'lucide-react';

interface ModulePlaceholderProps {
    title: string;
}

export const ModulePlaceholder: React.FC<ModulePlaceholderProps> = ({ title }) => {
    return (
        <Layout title={title}>
            <div className="placeholder-container">
                <Construction size={48} color="#0070f3" />
                <h2>{title} Module</h2>
                <p>This module is currently under development.</p>
            </div>

            <style>{`
        .placeholder-container {
          height: 60vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 16px;
          color: var(--text-secondary);
        }

        .placeholder-container h2 {
          color: var(--text-primary);
        }
      `}</style>
        </Layout>
    );
};
