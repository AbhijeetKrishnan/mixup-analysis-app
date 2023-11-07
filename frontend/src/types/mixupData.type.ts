export type MixupData = {
    title: string;
    comment: string;
    player_1: string;
    player_2: string;
    rows: number;
    cols: number;
    p1_strategies: string[];
    p2_strategies: string[];
    matrix: number[][];
    p1_probs: [number, number][] | null;
    p2_probs: [number, number][] | null;
    payoff: [number, number] | null;
};