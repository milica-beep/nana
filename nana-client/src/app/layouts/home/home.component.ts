import { Component } from '@angular/core';
import { Recipe } from 'src/app/models/recipe';
import { RecipeService } from 'src/app/services/recipe.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  latestRecipes: Recipe[] = [];
  page: number = 0;

  constructor(private recipeService: RecipeService) {}

  ngOnInit() {
    this.recipeService.getRecipes(this.page).subscribe(res => {
      this.latestRecipes = res['recipes'];

      this.latestRecipes.map(el => {
        el['timestamp'] = new Date(el['timestamp']['$date'])
      })

      console.log(this.latestRecipes)
    })
  }

}
