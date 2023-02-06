import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { Recipe } from 'src/app/models/recipe';
import { AuthService } from 'src/app/services/auth.service';
import { RecipeService } from 'src/app/services/recipe.service';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css']
})
export class SearchResultComponent {
  result: Recipe[] = [];
  query: any;
  currentUserId: any;

  constructor(private recipeService: RecipeService,
              private authService: AuthService,
              private route: ActivatedRoute,
              private router: Router,
              private _snackBar: MatSnackBar) { }

  ngOnInit(): void { 
    this.route.paramMap.subscribe(params => {
      this.query = params.get('query');
      this.recipeService.search(this.query).subscribe(res => {
        this.result = res['recipes'];
      })
    });

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

  onDelete(recipeId: any) {
    this.recipeService.deleteRecipe(recipeId).subscribe(res => {
      this.recipeService.search(this.query).subscribe(res => {
        this.result = res['recipes'];
      })
    })
  }
}
