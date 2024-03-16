import { Component, OnInit } from '@angular/core';
import { Recipe } from '../recipe';
import { RecipeService } from '../recipe.service';
import { IngredientForRecipe } from '../ingredient-for-recipe';
import { AllowedUnits } from '../ingredient';

@Component({
  selector: 'app-add-recipe',
  templateUrl: './add-recipe.component.html',
  styleUrl: './add-recipe.component.css',

})

export class AddRecipeComponent implements OnInit {
  constructor(
    private recipeService: RecipeService) { }

  public recipe!: Recipe;
  public allowedUnits = AllowedUnits;

  initializeRecipe(): void {
    this.recipe = {
      name: "",
      veggie: false,
      ingredients: [this.addEmptyIngredient()]
    }
  }

  addEmptyIngredient(): IngredientForRecipe {
    return {
      ingredient: {
        name: "",
        unit: ""
      },
      amount: 0
    }
  }

  addRow(): void {
    this.recipe.ingredients.push(this.addEmptyIngredient())
  }

  removeIngredient(): void {
    this.recipe.ingredients.pop()
  }

  addRecipe(): void {
    if (!this.recipe.name && !this.recipe.ingredients[0].ingredient.name) { return; }
    this.recipeService.addRecipe(this.recipe).subscribe()
    this.initializeRecipe();


  }

  ngOnInit(): void {
    this.initializeRecipe();
  }
}