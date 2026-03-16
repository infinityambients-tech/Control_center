import React, { useEffect, useMemo, useState } from 'react';
import { Layout } from '../../components/Layout';

type UpdateEvent =
  | { type: 'checking' }
  | { type: 'available'; info?: any }
  | { type: 'none'; info?: any }
  | { type: 'progress'; progress?: any }
  | { type: 'downloaded'; info?: any }
  | { type: 'error'; error: string };

declare global {
  interface Window {
    ipcRenderer?: {
      on: (channel: string, listener: (event: any, ...args: any[]) => void) => any;
      off: (channel: string, listener: (event: any, ...args: any[]) => void) => any;
      invoke: (channel: string, ...args: any[]) => Promise<any>;
    };
  }
}

const Updates: React.FC = () => {
  const [version, setVersion] = useState<string>('—');
  const [status, setStatus] = useState<string>('Gotowe');
  const [progress, setProgress] = useState<string>('');
  const [canDownload, setCanDownload] = useState<boolean>(false);
  const [canInstall, setCanInstall] = useState<boolean>(false);

  const isElectron = useMemo(() => Boolean(window.ipcRenderer?.invoke), []);

  useEffect(() => {
    if (!isElectron) return;
    window.ipcRenderer!.invoke('updates:getVersion').then((v) => setVersion(String(v))).catch(() => {});

    const handler = (_evt: any, payload: UpdateEvent) => {
      if (!payload || typeof payload !== 'object') return;
      if (payload.type === 'checking') {
        setStatus('Sprawdzanie aktualizacji…');
        setProgress('');
        setCanDownload(false);
        setCanInstall(false);
      } else if (payload.type === 'available') {
        setStatus('Dostępna aktualizacja.');
        setCanDownload(true);
      } else if (payload.type === 'none') {
        setStatus('Brak aktualizacji.');
        setCanDownload(false);
        setCanInstall(false);
      } else if (payload.type === 'progress') {
        const p = payload.progress || {};
        const pct = typeof p.percent === 'number' ? `${p.percent.toFixed(1)}%` : '';
        const speed = typeof p.bytesPerSecond === 'number' ? `${Math.round(p.bytesPerSecond / 1024)} KB/s` : '';
        setStatus('Pobieranie…');
        setProgress([pct, speed].filter(Boolean).join(' • '));
      } else if (payload.type === 'downloaded') {
        setStatus('Pobrano. Możesz zainstalować.');
        setProgress('');
        setCanDownload(false);
        setCanInstall(true);
      } else if (payload.type === 'error') {
        setStatus(`Błąd: ${payload.error}`);
        setCanDownload(false);
        setCanInstall(false);
      }
    };

    window.ipcRenderer!.on('updates:event', handler);
    return () => {
      window.ipcRenderer!.off('updates:event', handler);
    };
  }, [isElectron]);

  const check = async () => {
    if (!isElectron) return;
    try {
      await window.ipcRenderer!.invoke('updates:check');
    } catch (e: any) {
      setStatus(`Błąd: ${String(e?.message || e)}`);
    }
  };

  const download = async () => {
    if (!isElectron) return;
    try {
      await window.ipcRenderer!.invoke('updates:download');
    } catch (e: any) {
      setStatus(`Błąd: ${String(e?.message || e)}`);
    }
  };

  const install = async () => {
    if (!isElectron) return;
    try {
      await window.ipcRenderer!.invoke('updates:install');
    } catch (e: any) {
      setStatus(`Błąd: ${String(e?.message || e)}`);
    }
  };

  return (
    <Layout title="Updates">
      <div className="card" style={{ maxWidth: 720 }}>
        <h2>Auto-update</h2>
        {!isElectron ? (
          <p>Ta funkcja jest dostępna tylko w wersji desktop (Electron).</p>
        ) : (
          <>
            <p><strong>Wersja:</strong> {version}</p>
            <p><strong>Status:</strong> {status}</p>
            {progress && <p><strong>Postęp:</strong> {progress}</p>}
            <div style={{ display: 'flex', gap: 12, marginTop: 12 }}>
              <button className="btn" onClick={check}>Sprawdź</button>
              <button className="btn" onClick={download} disabled={!canDownload}>Pobierz</button>
              <button className="btn" onClick={install} disabled={!canInstall}>Zainstaluj</button>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
};

export default Updates;
