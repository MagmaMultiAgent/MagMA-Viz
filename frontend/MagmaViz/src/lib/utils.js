export async function GET(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
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

    let red = Math.abs(red_hash % 256);
    let green = Math.abs(green_hash % 256);
    let blue = Math.abs(blue_hash % 256);

    return `rgb(${red}, ${green}, ${blue})`;
}
