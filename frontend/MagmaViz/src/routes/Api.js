import { POST, API_URL } from '$lib/utils.js';

export async function saveData() {
    try {
        return await POST(`${API_URL}/saveData`)
    } catch (error) {
        console.error('Error saving data:', error);
        throw error;
    }
}

export async function loadData(filePath) {
    console.log("filePath:", filePath);
    let fileName = filePath.split('/')[filePath.split('/').length - 1].split('\\')[filePath.split('\\').length - 1];
    console.log("fileName:", fileName);
    try {
        return await POST(`${API_URL}/loadData?name=${fileName}`)
    } catch (error) {
        console.error('Error loading data:', error);
        throw error;
    }
}
