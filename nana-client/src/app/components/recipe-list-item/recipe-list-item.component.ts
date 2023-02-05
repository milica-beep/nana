import { Component, Input, OnInit } from '@angular/core';
import { Recipe } from 'src/app/models/recipe';
import { RecipeService } from 'src/app/services/recipe.service';

@Component({
  selector: 'app-recipe-list-item',
  templateUrl: './recipe-list-item.component.html',
  styleUrls: ['./recipe-list-item.component.css']
})
export class RecipeListItemComponent implements OnInit {
  @Input('recipe') recipe!: Recipe;
  @Input('currentUserId') currentUserId!: string;

  constructor(private recipeService: RecipeService) { }

  ngOnInit(): void {
  }

  onDelete() {
    // this.recipeService.deleteRecipe(this.recipe.id).subscribe(response => {
    //   console.log(response);
    // })
  }

}