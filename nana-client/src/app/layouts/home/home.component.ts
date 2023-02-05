import { Component } from '@angular/core';
import { Category } from 'src/app/models/category';
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
  categories: Category[] = [];
  selectedFilter: string = "";

  constructor(private recipeService: RecipeService) {}

  ngOnInit() {
    this.recipeService.getRecipes(this.page).subscribe(res => {
      this.latestRecipes = res['recipes'];

      this.latestRecipes.map(el => {
        el['timestamp'] = new Date(el['timestamp']['$date'])
      })

      console.log(this.latestRecipes)
    })
    this.recipeService.getCategories().subscribe(res =>{
      this.categories = res['categories'];
    })
  }

  filterByCategory(catId: any) {
    if(this.selectedFilter != catId) {
      this.selectedFilter = catId;
      this.recipeService.getRecipesByCategory(this.page, catId['$oid']).subscribe(res => {
        this.latestRecipes = res['recipes'];
      })
    } else if(this.selectedFilter == catId ){
      this.selectedFilter = "";
      this.page = 0;
      this.recipeService.getRecipes(this.page).subscribe(res => {
        this.latestRecipes = res['recipes'];
      })
    }
  }

}
