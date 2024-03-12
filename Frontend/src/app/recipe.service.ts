import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Observable, catchError, of, tap } from 'rxjs';
import { Recipe } from './recipe';
import { ToastService } from './toast.service';
import { ToastType } from './toast';


@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  public recipeUrl: string = '/api/recipes/';

  log(logString: string): void {
    console.log(logString)
  }

  constructor(
    private http: HttpClient,
    private toastService: ToastService
  ) { }

  public toastType = ToastType

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };


  getRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(this.recipeUrl).pipe(
      tap(_ => this.log(`successfully fetched ${_.length} ingredients`)),
      catchError(this.handleError<Recipe[]>('getIngredients', []))
    )
  }

  getRecipe(id: number): Observable<Recipe> {
    const singleRecipeUrl = `${this.recipeUrl}/${id}`
    return this.http.get<Recipe>(singleRecipeUrl).pipe(
      tap(_ => this.log(`successfully fetched recipe with ${id} with its ${_.ingredients.length} ingredients`)),
      catchError(this.handleError<Recipe>('getRecipe'))
    )
  }

  addRecipe(recipe: Recipe): Observable<Recipe> {
    return this.http.post<Recipe>(this.recipeUrl, recipe, this.httpOptions).pipe(
      tap((newRecipe: Recipe) => this.log(`added recipe w/ id=${newRecipe.id}`)),
      tap(_ => this.toastService.addToast('Success', `Recipe ${_.name} successfully added`, this.toastType.Success)),
      catchError(this.handleError<Recipe>('addRecipe'))
    );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      console.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
