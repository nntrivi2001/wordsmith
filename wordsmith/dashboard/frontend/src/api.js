/**
 * API request utility functions
 */

const BASE = '';  // dev: vite proxy forwards to FastAPI

export async function fetchJSON(path, params = {}) {
    const url = new URL(path, window.location.origin);
    Object.entries(params).forEach(([k, v]) => {
        if (v !== undefined && v !== null) url.searchParams.set(k, v);
    });
    const res = await fetch(url.toString());
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    return res.json();
}

/**
 * Subscribe to SSE real-time event stream
 * @param {function} onMessage  callback when data is received
 * @param {{onOpen?: function, onError?: function}} handlers connection status callbacks
 * @returns {function} unsubscribe function
 */
export function subscribeSSE(onMessage, handlers = {}) {
    const { onOpen, onError } = handlers
    const es = new EventSource(`${BASE}/api/events`);
    es.onopen = () => {
        if (onOpen) onOpen()
    };
    es.onmessage = (e) => {
        try {
            onMessage(JSON.parse(e.data));
        } catch { /* ignore parse errors */ }
    };
    es.onerror = (e) => {
        // EventSource auto-reconnects, we only update connection status here
        if (onError) onError(e)
    };
    return () => es.close();
}
