import { ipcMain } from 'electron';
import keytar from 'keytar';

export function setupIpc() {
    // Secure Storage (Keytar) - Keep for session tokens/client-side secrets

    // Secure Storage (Keytar)
    ipcMain.handle('save-secret', async (_, { service, account, password }) => {
        await keytar.setPassword(service, account, password);
        return true;
    });

    ipcMain.handle('get-secret', async (_, { service, account }) => {
        return await keytar.getPassword(service, account);
    });

    ipcMain.handle('delete-secret', async (_, { service, account }) => {
        return await keytar.deletePassword(service, account);
    });
}
