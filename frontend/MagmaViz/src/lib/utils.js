export async function GET(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

export async function POST(url) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

export const HOST = "localhost:8000";
export const WS_URL = `ws://${HOST}/ws`;
export const API_URL = `http://${HOST}/api`;

export function connectWebSocket() {
    const clientId = Date.now();
    const ws = new WebSocket(`${WS_URL}/${clientId}`);
    ws.onopen = () => {
        console.log("websocket connected");
    };
    ws.onclose = () => {
        console.log("websocket disconnected");
    };
    ws.onerror = (error) => {
        console.log("error", error);
    };
    return ws;
}

export function checkIfNaN(value, default_value = -1) {
    if (isNaN(value)) {
        return default_value;
    }
    return value
}
export function getValueOrNone(value) {
    return value ? value : "none";
}

export const id = () => Math.random().toString(36).substring(2, 9);

export function hashCode(str) {
    let hash = 0;
    for (let i = 0, len = str.length; i < len; i++) {
        let chr = str.charCodeAt(i);
        hash = (hash << 5) - hash + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
}

export function getRGBFromHash(string) {
    let red_hash = hashCode(string + "_red");
    let green_hash = hashCode(string + "_green");
    let blue_hash = hashCode(string + "_blue");

    let red = Math.abs(red_hash % 224);
    let green = Math.abs(green_hash % 224);
    let blue = Math.abs(blue_hash % 224);

    return `rgb(${red}, ${green}, ${blue})`;
}

export const localStoragePrefixBase = "MagmaViz";

export function saveToLocalStorage(prefix, name, value) {
    localStorage.setItem(`${localStoragePrefixBase}$${prefix}$${name}`, value);
}

export function getFromLocalStorage(prefix, name) {
    return localStorage.getItem(`${localStoragePrefixBase}$${prefix}$${name}`);
}

export function getKeysFromLocalStorage(prefix) {
    prefix = `${localStoragePrefixBase}$${prefix}$`;
    return Object.keys(localStorage).filter(key => key.startsWith(prefix)).map(key => key.replace(prefix, ""));
}
