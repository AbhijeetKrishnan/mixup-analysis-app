import type { Actions } from './$types';
import type { MixupData } from '../types/mixupData.type';


const backendUrl = 'http://127.0.0.1:8000';


function buildStrategies(formData: FormData, name: string): string[] {
    const strategies = [];
    const num_strats = name === '1' ? Number(formData.get('rows')) : Number(formData.get('cols'));
    for (let i = 0; i < num_strats; i++) {
        const strategy = formData.get(`s${name}-${i}`);
        strategies.push(strategy as string);
    }
    return strategies;
}

function buildMatrix(formData: FormData): number[][] {
    const rows = Number(formData.get('rows'));
    const cols = Number(formData.get('cols'));
    const matrix = [];
    for (let i = 0; i < rows; i++) {
        const row = [];
        for (let j = 0; j < cols; j++) {
            const value = Number(formData.get(`cell-${i}-${j}`));
            row.push(value);
        }
        matrix.push(row);
    }
    return matrix;
}

function getMixupData(formData: FormData): MixupData {
    const title = formData.get('title') as string;
    const comment = formData.get('comment') as string;
    const player_1 = formData.get('player_1') as string;
    const player_2 = formData.get('player_2') as string;
    const rows = Number(formData.get('rows'));
    const cols = Number(formData.get('cols'));
    const p1_strategies = buildStrategies(formData, '1');
    const p2_strategies = buildStrategies(formData, '2');
    const matrix = buildMatrix(formData);
    return {
        title,
        comment,
        player_1,
        player_2,
        rows,
        cols,
        p1_strategies,
        p2_strategies,
        matrix,
    };
}

export const actions: Actions = {
    analyze: async ({ cookies, request }) => {
        const formData = await request.formData();
        const mixupData = getMixupData(formData);
        console.log(mixupData);
        const result = await fetch(`${backendUrl}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mixupData),
        });
        let analysisData = await result.json();
        return { "type": "analyze", "result": analysisData, "orig": mixupData };
    },
    download: async ({ cookies, request }) => {
        const formData = await request.formData();
        const mixupData = getMixupData(formData);
        console.log(mixupData);
        const result = await fetch(`${backendUrl}/download`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mixupData),
        });
        let text = await result.text();
        return { "type": "download", "result": text, "orig": mixupData };

    },
    upload: async ({ cookies, request }) => {
        const formData = await request.formData();
        const fileData = formData;
        const result = await fetch(`${backendUrl}/upload`, {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: JSON.stringify(fileData),
        });
        let mixupData = await result.json();
        return { "type": "upload", "result": mixupData, "orig": null };
    },
} satisfies Actions;