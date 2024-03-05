import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IngredientsComponent } from './ingredients/ingredients.component';
import { IngredientDetailComponent } from './ingredient-detail/ingredient-detail.component';

const routes: Routes = [
  {path: 'ingredients', component: IngredientsComponent},
  {path: '', redirectTo: '/ingredients', pathMatch: 'full' },
  {path: 'ingredients/:id', component: IngredientDetailComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
