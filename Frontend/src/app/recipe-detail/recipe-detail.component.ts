import { Component, OnInit } from '@angular/core';
import { RecipeService } from '../recipe.service';
import { Recipe } from '../recipe';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  styleUrl: './recipe-detail.component.css'
})
export class RecipeDetailComponent implements OnInit{
  recipe: Recipe | undefined;
  constructor(
    private recipeService: RecipeService,
    private route: ActivatedRoute) {}

  getRecipe(): void {
    const id = parseInt(this.route.snapshot.paramMap.get('id')!, 10)
    this.recipeService.getRecipe(id).subscribe(recipe => this.recipe = recipe)
  }

  ngOnInit(): void {
    this.getRecipe();
  }
}
