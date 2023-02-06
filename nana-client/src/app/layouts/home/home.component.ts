import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { Category } from 'src/app/models/category';
import { Recipe } from 'src/app/models/recipe';
import { AuthService } from 'src/app/services/auth.service';
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
  currentUserId: any;

  constructor(private recipeService: RecipeService,
              private authService: AuthService,
              private router: Router,
              private _snackBar: MatSnackBar) {}

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
    
     this.authService.getCurrentUser().subscribe({
      error: (e) => {
        this.router.navigateByUrl('');
        this._snackBar.open('You need to log in again!', 'Close');
      },
      next: (res) => {
        this.currentUserId = res['_id']['$oid']
      }  
    })
  }

  filterByCategory(catId: any) {
    if(this.selectedFilter != catId) {
      this.selectedFilter = catId;
      this.recipeService.getRecipesByCategory(this.page, catId['$oid']).subscribe(res => {
        this.latestRecipes = res['recipes'];
        this.latestRecipes.forEach(el => {
          console.log(el)
        })
      })
    } else if(this.selectedFilter == catId ){
      this.selectedFilter = "";
      this.page = 0;
      this.recipeService.getRecipes(this.page).subscribe(res => {
        this.latestRecipes = res['recipes'];
        this.latestRecipes.forEach(el => {
          console.log(el)
        })
      })
    }
  }

  onDelete(recipeId: any) {
    console.log(recipeId)
  }

}
