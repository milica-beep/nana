import { Category } from "./category";
import { Level } from "./level";

export class Recipe {
    userId: any;
    title!: string;
    ingredients: string[] = [];
    preparation!: string;
    prepTime!: string;
    briefSummary!: string;
    categories: Category[] = [];
    level: Level = new Level();
  }