export function createWebSocket() {
  return new WebSocket("ws://localhost:8000/ws");
}