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
  selectedFilter: any = "";
  currentUserId: any;

  disableLoadMore: boolean = false;

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
    this.page = 0;
    this.disableLoadMore = false;
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

  onDelete(recipeId: any) {
    this.recipeService.deleteRecipe(recipeId).subscribe(res => {
      this.page = 0;
      this.recipeService.getRecipes(this.page).subscribe(res => {
        this.latestRecipes = res['recipes'];
      })
    })
  }

  loadMore() {
    this.page = this.page + 1;
    if(this.selectedFilter != "") {
      this.recipeService.getRecipesByCategory(this.page, this.selectedFilter['$oid']).subscribe(res => {
        if(res['recipes'].length == 0) {
          this.disableLoadMore = true;
        }
        res['recipes'].forEach((element: Recipe) => {
          this.latestRecipes.push(element);
        });
      })
    }
    else {
      this.recipeService.getRecipes(this.page).subscribe(res => {
        if(res['recipes'].length == 0) {
          this.disableLoadMore = true;
        }
        res['recipes'].forEach((element: Recipe) => {
          this.latestRecipes.push(element);
        });
      })
    }
  }

}
