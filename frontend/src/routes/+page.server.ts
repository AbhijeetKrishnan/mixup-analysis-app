import type { Actions } from './$types';
import type { MixupData } from '../types/mixupData.type';


const backendUrl = 'http://127.0.0.1:8000';

function convertToTuple(value: FormDataEntryValue | null): [number, number] | null {
    if (value === null || typeof value !== 'string') {
      return null;
    }
  
    const parts = value.split(',').map(Number);
    return [parts[0], parts[1]] as [number, number];
  }

function convertToTupleArray(value: FormDataEntryValue | null): [number, number][] | null {
    if (value === null || typeof value === 'string' || value instanceof File) {
      return null;
    }
  
    return (value as string[]).map((str: string) => {
      const parts = str.split(',').map(Number);
      return [parts[0], parts[1]] as [number, number];
    });
  }

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
    const p1_probs = convertToTupleArray(formData.get('p1_probs'));
    const p2_probs = convertToTupleArray(formData.get('p2_probs'));
    const payoff = convertToTuple(formData.get('payoff'));
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
        p1_probs,
        p2_probs,
        payoff,
    };
}

export const actions: Actions = {
    analyze: async ({ cookies, request }) => {
        const data = await request.formData();
        console.log('Data', data);
        const mixupData = getMixupData(data);
        console.log('Matrix', JSON.stringify(mixupData));
        const result = await fetch(`${backendUrl}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mixupData),
        });
        console.log(result);
        return result.json();
    },
    download: async ({ cookies, request }) => {
        const data = await request.formData();
        const mixupData = getMixupData(data);
        console.log('Matrix', JSON.stringify(mixupData));
        const result = await fetch(`${backendUrl}/download`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mixupData),
        });
        console.log(result);
        return result.text();

    },
    upload: async ({ cookies, request }) => {
        const data = await request.formData();
        const mixupData = getMixupData(data);
        const result = await fetch(`${backendUrl}/upload`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mixupData),
        });
        console.log(result);
        return result.json();

    },
} satisfies Actions;