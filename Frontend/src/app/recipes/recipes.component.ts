import { Component, OnInit } from '@angular/core';
import { RecipeService } from '../recipe.service';
import { Recipe } from '../recipe';

@Component({
  selector: 'app-recipes',
  templateUrl: './recipes.component.html',
  styleUrl: './recipes.component.css'
})
export class RecipesComponent implements OnInit{
  recipes: Recipe[] = [];
  constructor(private recipeService: RecipeService) {}

  getRecipes(): void {
    this.recipeService.getRecipes().subscribe(recipes => this.recipes = recipes);
  }

  ngOnInit() {
    this.getRecipes();
  }
}
