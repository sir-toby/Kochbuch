import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IngredientsComponent } from './ingredients/ingredients.component';
import { IngredientDetailComponent } from './ingredient-detail/ingredient-detail.component';
import { RecipesComponent } from './recipes/recipes.component';
import { RecipeDetailComponent } from './recipe-detail/recipe-detail.component';


const routes: Routes = [
  {path: '', redirectTo: '/ingredients', pathMatch: 'full' },
  {path: 'ingredients', component: IngredientsComponent},
  {path: 'ingredients/:id', component: IngredientDetailComponent},
  {path: 'recipes', component: RecipesComponent},
  {path: 'recipes/:id', component: RecipeDetailComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
