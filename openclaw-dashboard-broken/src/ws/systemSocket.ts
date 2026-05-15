type Listener = (event: any) => void;

class SystemSocket {
  private ws: WebSocket | null = null;
  private listeners: Listener[] = [];

  connect() {
    if (this.ws) return;
    this.ws = new WebSocket("ws://localhost:8081/system/ws");

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.listeners.forEach((l) => l(data));
      } catch {}
    };

    this.ws.onclose = () => {
      this.ws = null;
      setTimeout(() => this.connect(), 2000);
    };
  }

  subscribe(listener: Listener) {
    this.listeners.push(listener);
    this.connect();
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }
}

export const systemSocket = new SystemSocket();
