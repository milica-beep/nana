# nana
Aplikacija namenjena pisanju i pretraživanju recepata. Razvijena korišćenjem *Flask* i *Angular* okruženja i *mongodb* baze podataka.

# Backend

Pokretanje:
1. Instalacija potrebnih modula korišćenjem pip packet manager-a
	```bash
	pip install -r requirements.txt
	```

2. Kreiranje i dodavanje podataka u bazu:
	```bash
	python create_data.py
	```
3. Pokretanje aplikacije: 
	```bash
	python app.py
	```
  
 ## Frontend
1. Instalacija Node.js-a i npm-a (https://nodejs.org/en/download/)
2. Instalacija Angular framework-a korišćenjem npm packet manager-a
	```bash
	npm install -g @angular/cli
	```
3. Pokretanje aplikacije
	```bash
	ng serve --open
	```
