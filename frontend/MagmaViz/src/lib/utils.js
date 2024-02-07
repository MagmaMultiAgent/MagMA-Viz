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