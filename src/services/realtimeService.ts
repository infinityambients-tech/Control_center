const WS_PROTOCOL = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const WS_BASE = `${WS_PROTOCOL}//${window.location.host}`;

type Handler = (payload: any) => void;

class RealtimeService {
  ws: WebSocket | null = null;
  handlers: Record<string, Set<Handler>> = {};

  connect(token?: string) {
    this.disconnect();
    const url = token ? `${WS_BASE}/ws?token=${encodeURIComponent(token)}` : `${WS_BASE}/ws`;
    this.ws = new WebSocket(url, []);

    this.ws.onopen = () => {
      console.debug('Realtime connected');
      this.isConnected = true;
      (this.handlers['connected'] || new Set()).forEach(h => h(true));
      // optional: send initial ping
      try { this.ws?.send('ping'); } catch (e) { }
    };

    this.ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data);
        const t = data.type || 'message';
        (this.handlers[t] || new Set()).forEach(h => h(data));
      } catch (e) {
        // if not JSON, ignore or handle ping/pong
        const text = evt.data;
        if (text === 'pong') return;
      }
    };

    this.ws.onclose = () => {
      console.debug('Realtime disconnected');
      this.isConnected = false;
      (this.handlers['disconnected'] || new Set()).forEach(h => h(false));
      this.ws = null;
    };

    this.ws.onerror = (e) => {
      console.error('Realtime error', e);
    };
  }

  isConnected: boolean = false;

  disconnect() {
    if (this.ws) {
      try { this.ws.close(); } catch (e) { }
      this.ws = null;
    }
  }

  on(event: string, handler: Handler) {
    this.handlers[event] = this.handlers[event] || new Set();
    this.handlers[event].add(handler);
  }

  off(event: string, handler?: Handler) {
    if (!this.handlers[event]) return;
    if (handler) this.handlers[event].delete(handler);
    else delete this.handlers[event];
  }

  emit(event: string, payload: any) {
    try {
      this.ws?.send(JSON.stringify({ type: event, payload }));
    } catch (e) {
      console.error('Realtime emit error', e);
    }
  }
}

export const realtimeService = new RealtimeService();
