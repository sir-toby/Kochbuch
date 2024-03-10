import { IngredientForRecipe } from "./ingredient-for-recipe"

export interface Recipe {
    id: number,
    name: string,
    veggie: boolean, 
    ingredients: [ingredientForRecipe: IngredientForRecipe]
}
