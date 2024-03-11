import { Component, OnInit } from '@angular/core';
import { Ingredient } from '../ingredient';
import { IngredientService } from '../ingredient.service';

@Component({
  selector: 'app-ingredients',
  templateUrl: './ingredients.component.html',
  styleUrl: './ingredients.component.css'
})
export class IngredientsComponent implements OnInit{
  ingredients:Ingredient[] = [];

  constructor(private ingredientService: IngredientService) {}

  getIngredients(): void {
    this.ingredientService.getIngredients().subscribe(ingredients => this.ingredients = ingredients)
  }

  ngOnInit() : void {
    this.getIngredients();
  }
}
