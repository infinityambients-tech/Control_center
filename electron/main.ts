import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { setupIpc } from './ipc.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// The built directory structure
// - dist/
//   - electron/
//     - main.js
//     - preload.js
//   - index.html

const DIST_PATH = path.join(__dirname, '../dist');
const VITE_PUBLIC_PATH = app.isPackaged ? DIST_PATH : path.join(DIST_PATH, '../public');

process.env.DIST = DIST_PATH;
process.env.VITE_PUBLIC = VITE_PUBLIC_PATH;

let win: BrowserWindow | null;
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL'];

function createWindow() {
    win = new BrowserWindow({
        icon: path.join(VITE_PUBLIC_PATH, 'electron-vite.svg'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.mjs'),
            nodeIntegration: false,
            contextIsolation: true,
        },
        width: 1200,
        height: 800,
    });

    // Test active push message to Renderer-process.
    win.webContents.on('did-finish-load', () => {
        win?.webContents.send('main-process-message', (new Date).toLocaleString());
    });

    if (VITE_DEV_SERVER_URL) {
        win.loadURL(VITE_DEV_SERVER_URL);
    } else {
        // win.loadFile('dist/index.html')
        win.loadFile(path.join(DIST_PATH, 'index.html'));
    }
}

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
        win = null;
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

setupIpc();

app.whenReady().then(createWindow);
