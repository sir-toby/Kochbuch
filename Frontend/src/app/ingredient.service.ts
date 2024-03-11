import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Ingredient } from './ingredient';
import { Observable, catchError, of, tap } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class IngredientService {

  private ingredientsUrl = '/api/ingredients/'

  log(logString: string): void {
    console.log(logString)
  }


  getIngredients(): Observable<Ingredient[]> {
    return this.http.get<Ingredient[]>(this.ingredientsUrl).pipe(
      tap(_ => this.log(`successfully fetched ${_.length} ingredients`)),
      catchError(this.handleError<Ingredient[]>('getIngredients', []))
    )
  }

  getIngredient(id: number): Observable<Ingredient> {
    return this.http.get<Ingredient>(`${this.ingredientsUrl}/${id}`).pipe(
      tap(_ => this.log(`successfully fetched ingredient with id ${_.id}`)),
      catchError(this.handleError<Ingredient>(`getIngredient id=${id}`))
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

  constructor(
    private http: HttpClient,
  ) { }
}
