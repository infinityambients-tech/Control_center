import React, { useState } from 'react';
import { Camera, Save } from 'lucide-react';

export const AccountSettings: React.FC = () => {
    const [avatar, setAvatar] = useState<string | null>(null);

    const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (event) => {
                if (event.target?.result) setAvatar(event.target.result as string);
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    };

    return (
        <div className="account-settings fade-in">
            <div className="settings-section">
                <h3>Profile Picture</h3>
                <p className="section-desc">Upload a high-res image to personalize your account.</p>

                <div className="avatar-upload-area">
                    <div className="avatar-preview">
                        {avatar ? (
                            <img src={avatar} alt="Avatar" />
                        ) : (
                            <div className="avatar-placeholder">
                                <Camera size={32} />
                            </div>
                        )}
                        <input
                            type="file"
                            accept="image/*"
                            className="file-input"
                            onChange={handleAvatarChange}
                            id="avatar-upload"
                        />
                        <label htmlFor="avatar-upload" className="upload-btn">
                            Change Picture
                        </label>
                    </div>
                </div>
            </div>

            <div className="settings-section">
                <h3>Personal Information</h3>
                <div className="form-grid">
                    <div className="form-group">
                        <label>First Name</label>
                        <input type="text" defaultValue="Admin" />
                    </div>
                    <div className="form-group">
                        <label>Last Name</label>
                        <input type="text" defaultValue="User" />
                    </div>
                    <div className="form-group full-width">
                        <label>Email Address</label>
                        <input type="email" defaultValue="admin@control-center.pl" disabled />
                    </div>
                </div>
            </div>

            <div className="settings-actions">
                <button className="btn-primary">
                    <Save size={18} />
                    Save Changes
                </button>
            </div>

            <style>{`
        .account-settings {
          display: flex;
          flex-direction: column;
          gap: 32px;
          max-width: 600px;
        }

        .settings-section {
          background: var(--bg-card);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 24px;
        }

        .settings-section h3 {
          font-size: 1.1rem;
          margin-bottom: 4px;
        }

        .section-desc {
          color: var(--text-secondary);
          font-size: 0.85rem;
          margin-bottom: 20px;
        }

        .avatar-upload-area {
          display: flex;
          align-items: center;
          gap: 24px;
        }

        .avatar-preview {
          display: flex;
          align-items: center;
          gap: 20px;
        }

        .avatar-preview img {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          object-fit: cover;
          border: 2px solid var(--border);
        }

        .avatar-placeholder {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.05);
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--text-secondary);
          border: 1px dashed var(--border);
        }

        .file-input {
          display: none;
        }

        .upload-btn {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border);
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9rem;
          font-weight: 500;
          transition: all 0.2s;
        }

        .upload-btn:hover {
          background: rgba(255, 255, 255, 0.1);
          border-color: var(--border-hover);
        }

        .form-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
        }

        .form-group {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }

        .form-group.full-width {
          grid-column: span 2;
        }

        .form-group label {
          font-size: 0.85rem;
          color: var(--text-secondary);
        }

        .form-group input {
          background: var(--bg-dark);
          border: 1px solid var(--border);
          padding: 10px;
          border-radius: 6px;
          color: white;
        }

        .form-group input:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .settings-actions {
          display: flex;
          justify-content: flex-end;
        }

        .btn-primary {
          background: var(--accent);
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          transition: transform 0.2s;
        }

        .btn-primary:hover {
          transform: translateY(-1px);
        }
      `}</style>
        </div>
    );
};
