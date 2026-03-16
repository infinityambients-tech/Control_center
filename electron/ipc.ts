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
    ipcMain.handle('updates:check', async () => {
        if (!app.isPackaged) throw new Error('Updates available only in packaged build');
        await autoUpdater.checkForUpdates();
        return true;
    });
    ipcMain.handle('updates:download', async () => {
        if (!app.isPackaged) throw new Error('Updates available only in packaged build');
        await autoUpdater.downloadUpdate();
        return true;
    });
    ipcMain.handle('updates:install', async () => {
        if (!app.isPackaged) throw new Error('Updates available only in packaged build');
        autoUpdater.quitAndInstall();
        return true;
    });
}
