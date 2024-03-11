import { Component } from '@angular/core';
import { Recipe } from '../recipe';
import { RecipeService } from '../recipe.service';
import { IngredientForRecipe } from '../ingredient-for-recipe';


@Component({
  selector: 'app-add-recipe',
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css',

})
export class AddRecipeComponent {
  constructor(private recipeService: RecipeService) { };

  recipe: Recipe = {
    name: "",
    veggie: false,
    ingredients: [this.generateEmptyIngredient()]
  }

  generateEmptyIngredient(): IngredientForRecipe {
    return {
      ingredient: {
        name: "",
        unit: ""
      },
      amount: 0
    }
  }


  addRow(): void {
    this.recipe.ingredients.push(this.generateEmptyIngredient())
  }

  removeRow(): void {
    this.recipe.ingredients.pop()
  }

  addRecipe(): void {
    // if (!this.recipe.name && !this.recipe.ingredients[0].ingredient.name) {return; }

    console.log(this.recipe)
    this.recipeService.addRecipe(this.recipe).subscribe(newRecipe => this.recipe = newRecipe)
  }
}