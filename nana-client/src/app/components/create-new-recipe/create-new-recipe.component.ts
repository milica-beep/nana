import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Category } from 'src/app/models/category';
import { Level } from 'src/app/models/level';
import { Recipe } from 'src/app/models/recipe';
import { RecipeService } from 'src/app/services/recipe.service';

@Component({
  selector: 'app-create-new-recipe',
  templateUrl: './create-new-recipe.component.html',
  styleUrls: ['./create-new-recipe.component.css']
})
export class CreateNewRecipeComponent {
  recipeForm!: FormGroup;
  ingredients: string[] = [];
  all_categories: Category[] = [];
  selected_categories: Category[] = [];
  levels: Level[] = [];

  constructor(private formBuilder: FormBuilder,
    private recipeService: RecipeService,
    private router: Router) { }

ngOnInit(): void {
  this.recipeForm = this.formBuilder.group({
    title: ['', Validators.required],
    ingredient: [''],
    preparation: ['', Validators.required],
    prepTime: [''],
    briefSummary: ['', Validators.required],
    categories: [''],
    level: ['']
  });

  this.recipeService.getCategories().subscribe(res =>{
    this.all_categories = res['categories'];
  })

  this.recipeService.getLevels().subscribe(res => {
    this.levels = res['levels'];
  })
}

get f() { return this.recipeForm.controls; }

addIngredient() {
  if(this.f["ingredient"].value == "") {
    return;
  }
  let tmp = this.ingredients.filter(x => x == this.f["ingredient"].value);
  if(tmp.length == 0) {
    this.ingredients.push(this.f["ingredient"].value);
    this.f["ingredient"].setValue("");
  }
}

onSubmit() {
  if (this.recipeForm.invalid) {
  return;
  }

  let new_recipe: Recipe = new Recipe();
  new_recipe.title = this.f["title"].value;
  new_recipe.ingredients = this.ingredients;
  new_recipe.preparation = this.f["preparation"].value;
  new_recipe.prepTime = this.f["prepTime"].value;
  new_recipe.briefSummary = this.f["briefSummary"].value;
  new_recipe.categories = this.f["categories"].value;
  new_recipe.level = this.f["level"].value;

  console.log("New recipe:", new_recipe);

  this.recipeService.postRecipe(new_recipe).subscribe(
    {
      error: (e) => console.error(e),
      complete: () => {
        console.info('complete')
        //this.router.navigateByUrl('/home');
      }  
    })
  }


}
