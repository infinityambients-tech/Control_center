import { ipcRenderer, contextBridge } from 'electron';

// --------- Expose some API to the Renderer process ---------
contextBridge.exposeInMainWorld('ipcRenderer', {
    on(...args: Parameters<typeof ipcRenderer.on>) {
        const [channel, listener] = args;
        return ipcRenderer.on(channel, (event, ...args) => listener(event, ...args));
    },
    off(...args: Parameters<typeof ipcRenderer.off>) {
        const [channel, ...rest] = args;
        return ipcRenderer.off(channel, ...rest);
    },
    send(...args: Parameters<typeof ipcRenderer.send>) {
        const [channel, ...rest] = args;
        return ipcRenderer.send(channel, ...rest);
    },
    invoke(...args: Parameters<typeof ipcRenderer.invoke>) {
        const [channel, ...rest] = args;
        return ipcRenderer.invoke(channel, ...rest);
    },

    // You can expose other apts you need here.
    // ...
});

contextBridge.exposeInMainWorld('api', {
    saveSecret: (data: any) => ipcRenderer.invoke('save-secret', data),
    getSecret: (data: any) => ipcRenderer.invoke('get-secret', data),
    deleteSecret: (data: any) => ipcRenderer.invoke('delete-secret', data),
});
