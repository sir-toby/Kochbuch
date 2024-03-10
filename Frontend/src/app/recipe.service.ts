import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Observable, catchError, of, tap } from 'rxjs';
import { Recipe } from './recipe';


@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  public recipesUrl: string = '/api/recipes/';

  log(logString: string): void {
    console.log(logString)
  }

  constructor(
    private http: HttpClient,
  ) { }

  getRecipes(): Observable<Recipe[]> {
    return this.http.get<Recipe[]>(this.recipesUrl).pipe(
      tap(_ => this.log(`successfully fetched ${_.length} ingredients`)),
      catchError(this.handleError<Recipe[]>('getIngredients', []))
    )
  }

  getRecipe(id: number): Observable<Recipe> {
    const singleRecipeUrl = `${this.recipesUrl}/${id}`
    return this.http.get<Recipe>(singleRecipeUrl).pipe(
      tap(_ => this.log(`successfully fetched recipe with ${id} with its ${_.ingredients.length} ingredients`)),
      catchError(this.handleError<Recipe>('getRecipe'))
    )
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
