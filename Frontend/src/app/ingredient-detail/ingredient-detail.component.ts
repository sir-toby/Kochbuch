import { Component, OnInit } from '@angular/core';

import { Ingredient } from '../ingredient';
import { IngredientService } from '../ingredient.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-ingredient-detail',
  templateUrl: './ingredient-detail.component.html',
  styleUrl: './ingredient-detail.component.css'
})
export class IngredientDetailComponent implements OnInit {
  ingredient : Ingredient | undefined

  constructor(
    private ingredientService: IngredientService,
    private route: ActivatedRoute
    ) {};

  getIngredient(): void {
    const id = parseInt(this.route.snapshot.paramMap.get('id')!, 10)
    this.ingredientService.getIngredient(id).subscribe(ingredient => this.ingredient=ingredient)
  }
  
  ngOnInit(): void {
    this.getIngredient()
  }

}
