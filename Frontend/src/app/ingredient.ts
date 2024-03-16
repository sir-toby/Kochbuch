export interface Ingredient {
    id?: number;
    name: string;
    unit: string;
}

export enum AllowedUnits {
    g = "g",
    ml = "mL",
    el = "EL",
    tl = "TL",
    stk = "Stk",
}