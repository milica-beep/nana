import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Recipe } from '../models/recipe';

@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  serverUrl:string = "http://127.0.0.1:5000/";

  constructor(private http: HttpClient) { }

  getCategories() {
    return this.http.get<any>(this.serverUrl + 'recipe/get-categories')
  }

  getLevels() {
    return this.http.get<any>(this.serverUrl + 'recipe/get-levels')
  }

  postRecipe(recipe:Recipe) {
    return this.http.post(this.serverUrl + 'recipe/create', recipe);
  }

  getRecipes() {
    return this.http.get<any>(this.serverUrl + "recipe/get-all-recipes");
  }

  getRecipe(recipeId: string) {
    let params = new HttpParams().set("id", recipeId.toString());
    return this.http.get<any>(this.serverUrl + "recipe/get-recipe", {params:params});
  }

  updateRecipe(recipe:Recipe) {
    return this.http.post(this.serverUrl + 'recipe/update-recipe', recipe);
  }

  deleteRecipe(recipeId: string) {
    let params = new HttpParams().set("id", recipeId.toString());
    return this.http.delete<any>(this.serverUrl + 'recipe/delete-recipe', {params:params});
  }
}