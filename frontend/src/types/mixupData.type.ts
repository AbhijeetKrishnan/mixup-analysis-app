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
};

export const mixupInitVal: MixupData = {
    title: '',
    comment: '',
    player_1: '',
    player_2: '',
    rows: 2,
    cols: 2,
    p1_strategies: ['', ''],
    p2_strategies: ['', ''],
    matrix: [
        [0, 0],
        [0, 0]
    ]
};

export type AnalysisData = {
    p1_probs: [number, number][];
    p2_probs: [number, number][];
    payoff: [number, number];
};
