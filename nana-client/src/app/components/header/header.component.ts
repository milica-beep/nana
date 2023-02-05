import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  searchForm!: FormGroup;
  searchQuery: string = "";
  constructor(private formBuilder: FormBuilder,
              private router: Router
              ) { }

  ngOnInit(): void {
    this.searchForm = this.formBuilder.group({
      search: ['', Validators.required]
    });
  }

  get f() { return this.searchForm.controls; }
  search() {
    this.searchQuery = this.f["search"].value;
    console.log("Search query u header", this.searchQuery);   
  }
}