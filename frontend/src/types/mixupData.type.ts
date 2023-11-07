export type MixupData = {
    title: string;
    comment: string;
    player_1: string;
    player_2: string;
    rows: number;
    cols: number;
    p1_strategies: string[];
    p2_strategies: string[];
    data: number[][];
    p1_probs: number[] | null;
    p2_probs: number[] | null;
    payoff: number | null;
};