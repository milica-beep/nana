import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CreateNewRecipeComponent } from './components/create-new-recipe/create-new-recipe.component';
import { EditRecipeComponent } from './components/edit-recipe/edit-recipe.component';
import { HomeComponent } from './layouts/home/home.component';
import { LandingComponent } from './layouts/landing/landing.component';
import { RecipeComponent } from './layouts/recipe/recipe.component';

const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'home', component: HomeComponent },
  { path: 'add-new-recipe', component: CreateNewRecipeComponent},
  { path: 'recipe/:id', component: RecipeComponent },
  { path: 'edit-recipe/:id', component: EditRecipeComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
