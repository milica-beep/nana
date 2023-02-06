import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Category } from 'src/app/models/category';
import { Level } from 'src/app/models/level';
import { Recipe } from 'src/app/models/recipe';
import { RecipeService } from 'src/app/services/recipe.service';

@Component({
  selector: 'app-edit-recipe',
  templateUrl: './edit-recipe.component.html',
  styleUrls: ['./edit-recipe.component.css']
})
export class EditRecipeComponent implements OnInit {
  recipeForm!: FormGroup;
  recipe!: Recipe;
  recipeId: any = "";

  ingredients: string[] = [];
  all_categories: Category[] = [];
  selected_categories: Category[] = [];
  levels: Level[] = [];
  
  addedIngredient: boolean = false;
  selectedLevel: Level = new Level();

  constructor(private formBuilder: FormBuilder,
    private recipeService: RecipeService,
    private router: Router,
    private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.recipeForm = this.formBuilder.group({
      title: ['', Validators.required],
      ingredient: [''],
      preparation: ['', Validators.required],
      preparationTime: [''],
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

    this.route.paramMap.subscribe(params => {
      this.recipeId = params.get('id') 
    });

    this.recipeService.getRecipe(this.recipeId).subscribe((response) => {
      this.recipe = response;
      let recipeFormData = {
        title: this.recipe.title,
        preparation: this.recipe.preparation,
        preparationTime: this.recipe.preparationTime,
        briefSummary: this.recipe.briefSummary,
        categories: this.recipe.categories.map(el => el = el['_id']['$oid']),
        ingredient: "",
        level: this.recipe.level._id['$oid']
      };
      this.ingredients = this.recipe.ingredients;

      this.recipeForm.setValue(recipeFormData);
    })
  }

  get f() { return this.recipeForm.controls; }

  addIngredient() {
    if(this.f["ingredient"].value == "") {
      return;
    }
    let tmp = this.ingredients.filter(x => x == this.f["ingredient"].value);
    if(tmp.length == 0) {
      this.addedIngredient = true;
      this.ingredients.push(this.f["ingredient"].value);
      this.f["ingredient"].setValue("");
    }
  }

  onSubmit() {
    if (this.recipeForm.invalid) {
      return;
    }

    if(!this.checkIfDataHasChanged()) {
      console.log("Form is touched : ", this.checkIfDataHasChanged());
      this.router.navigateByUrl('/home');
    }

    
    this.recipe.title = this.f["title"].value;
    this.recipe.ingredients = this.ingredients;
    this.recipe.preparation = this.f["preparation"].value;
    this.recipe.preparationTime = this.f["preparationTime"].value;
    this.recipe.briefSummary = this.f["briefSummary"].value;

    let lvl:any = this.levels.find(el => el._id['$oid'] == this.f["level"].value);
    this.recipe.level = lvl;

    let cats: any = [];
    this.f["categories"].value.forEach((element: any) => {
      this.all_categories.forEach(el => {
        if(el._id['$oid'] == element) {
          cats.push(el)
        }
      })
      
    });
    this.recipe.categories = cats;
   

    this.recipeService.updateRecipe(this.recipe)
      .subscribe(
        {
          error: (e) => console.error(e),
          complete: () => {
            console.info('complete')
            this.router.navigateByUrl('/home');
          }  
        }
      )
  }

  checkIfDataHasChanged() {
    console.log('rec ing', this.recipe.ingredients);
    console.log('this ing', this.ingredients)

    if(this.recipe.title != this.f['title'].value)
      return true;
    if(this.recipe.briefSummary != this.f['briefSummary'].value)
      return true;
    if(this.recipe.preparation != this.f['preparation'].value)
      return true;
    if(this.recipe.preparationTime != this.f['preparationTime'].value)
      return true;
    if(this.addedIngredient)
      return true;
    if(this.recipe.level['_id']['$oid'] != this.f['level'].value)
      return true;

    let flag = true;
    if(this.recipe.categories.length != this.f['categories'].value.length) {
      return true;
    }
    this.recipe.categories.forEach(el => {
      if(this.f['categories'].value.find((cat: any) => cat == el._id['$oid'])) {
        console.log('ima');
      }
      else {
        flag = false;
      }
    })
    if(!flag) {
      return true;
    }
    return false;
  }

}