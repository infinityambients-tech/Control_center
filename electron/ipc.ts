import { app, ipcMain, safeStorage } from 'electron';
import fs from 'node:fs';
import path from 'node:path';
import { autoUpdater } from 'electron-updater';

type KeytarLike = {
    setPassword(service: string, account: string, password: string): Promise<void>;
    getPassword(service: string, account: string): Promise<string | null>;
    deletePassword(service: string, account: string): Promise<boolean>;
};

async function tryLoadKeytar(): Promise<KeytarLike | null> {
    try {
        const mod = await import('keytar');
        // keytar may be cjs default export depending on build tooling
        return (mod as any).default ?? (mod as any);
    } catch {
        return null;
    }
}

function secretsPath() {
    return path.join(app.getPath('userData'), 'secrets.json');
}

function loadSecrets(): Record<string, string> {
    const p = secretsPath();
    if (!fs.existsSync(p)) return {};
    try {
        return JSON.parse(fs.readFileSync(p, 'utf-8')) || {};
    } catch {
        return {};
    }
}

function saveSecrets(data: Record<string, string>) {
    const p = secretsPath();
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, JSON.stringify(data, null, 2), 'utf-8');
}

export function setupIpc() {
    // Secure Storage (Keytar) - Keep for session tokens/client-side secrets

    // Secure Storage (Keytar)
    ipcMain.handle('save-secret', async (_, { service, account, password }) => {
        const keytar = await tryLoadKeytar();
        if (keytar) {
            await keytar.setPassword(service, account, password);
            return true;
        }
        if (!safeStorage.isEncryptionAvailable()) throw new Error('safeStorage encryption not available');
        const key = `${service}:${account}`;
        const secrets = loadSecrets();
        secrets[key] = safeStorage.encryptString(String(password)).toString('base64');
        saveSecrets(secrets);
        return true;
    });

    ipcMain.handle('get-secret', async (_, { service, account }) => {
        const keytar = await tryLoadKeytar();
        if (keytar) return await keytar.getPassword(service, account);
        const key = `${service}:${account}`;
        const secrets = loadSecrets();
        const enc = secrets[key];
        if (!enc) return null;
        try {
            return safeStorage.decryptString(Buffer.from(enc, 'base64'));
        } catch {
            return null;
        }
    });

    ipcMain.handle('delete-secret', async (_, { service, account }) => {
        const keytar = await tryLoadKeytar();
        if (keytar) return await keytar.deletePassword(service, account);
        const key = `${service}:${account}`;
        const secrets = loadSecrets();
        const existed = Object.prototype.hasOwnProperty.call(secrets, key);
        delete secrets[key];
        saveSecrets(secrets);
        return existed;
    });

    // Auto-update (electron-updater)
    ipcMain.handle('updates:getVersion', () => app.getVersion());
    ipcMain.handle('updates:check', async (event) => {
        if (!app.isPackaged) {
            // Mock update process for development visualization
            event.sender.send('updates:event', { type: 'checking' });
            setTimeout(() => {
                if (!event.sender.isDestroyed()) {
                    event.sender.send('updates:event', { 
                        type: 'available', 
                        info: { version: '0.1.3' } 
                    });
                }
            }, 1000);
            return { success: true };
        }
        await autoUpdater.checkForUpdates();
        return { success: true };
    });
    ipcMain.handle('updates:download', async (event) => {
        if (!app.isPackaged) {
            // Mock download progress for development visualization
            let percent = 0;
            const interval = setInterval(() => {
                if (event.sender.isDestroyed()) {
                    clearInterval(interval);
                    return;
                }
                percent += 20;
                if (percent <= 100) {
                    event.sender.send('updates:event', { 
                        type: 'progress', 
                        progress: { percent, bytesPerSecond: 1024 * 512 } 
                    });
                }
                if (percent >= 100) {
                    clearInterval(interval);
                    event.sender.send('updates:event', { type: 'downloaded' });
                }
            }, 500);
            return { success: true };
        }
        await autoUpdater.downloadUpdate();
        return { success: true };
    });
    ipcMain.handle('updates:install', async () => {
        if (!app.isPackaged) {
            const { dialog } = await import('electron');
            await dialog.showMessageBox({
                type: 'info',
                title: 'Symulacja Instalacji',
                message: 'W wersji produkcyjnej aplikacja zostałaby teraz zamknięta i zainstalowana nowa wersja.',
                buttons: ['OK']
            });
            return { success: true };
        }
        autoUpdater.quitAndInstall();
        return { success: true };
    });
}
