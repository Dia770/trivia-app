# Trivia APP

Ce projet est un devoir du parcours full stack development using Flask (UDACITY), j'ai pris plaisir a le realiser.
C'est une application qui contient des questions et réponses et permet de lancer un quiz. 

L'application doit :
- Afficher les questions - toutes les questions et par catégorie. Les questions doivent afficher la question, la catégorie et le degré de difficulté par défaut et peuvent afficher ou masquer la réponse.
- Supprimer les questions.
- Ajouter des questions et exiger qu'elles comprennent le texte de la question et de la réponse.
- Rechercher des questions à partir d'une chaîne de texte de requête.
Jouer le questionnaire en randomisant toutes les questions ou dans une catégorie spécifique.

## Commencez

### Pre-requis et Developpement Local 
Python3, pip et node.js doivent etre installés au prealable .

#### Backend

Depuis le dossier backen, executez `pip install requirements.txt`. Tous les packages sont inclus dans requirements.txt. 

Pour lancer l'application, entrez les commandes suivantes : 
(si vous etes sur windows)
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

L'application demarre sur `http://127.0.0.1:5000/` par defaut et sert de proxy dans la configuration du frontend. 

#### Frontend

Depuis le dossier frontend, lancez les commandes suivantes pour lancer le client 
```
npm install // seulement une fois pour installer dependances
npm start 
```

Par defaut le frontend est sur localhost:3000. 


## Réference de l'API 

### Commencez
- URL: `http://127.0.0.1:5000/`
- Authentication: Cette version ne supporte pas l'authenfication

### Gestion d'erreurs
Les erreurs sont retournes en object json dans les formats suivants :
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
Listes des erreurs :
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Points de terminaisons 
#### GET /questions
- General:
    - Retourne la liste des questions, les categories, un success et le nombre total de questions
    - Le resultat est rendu sur plusieurs page. Chaque page contient 10 pages. Inclus un argument pour choisir le numero de page, qui commence par 1 
- Exemple: `curl http://127.0.0.1:5000/questions`

``` 
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

#### GET /categories
- General:
    - Retourne la liste les categories, et un success 
- Exemple: `curl http://127.0.0.1:5000/categories`

``` 
{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /categories/<int:categorie_id>/questions
- General:
    - Retourne la liste les questions pour une categorie, le nom de la categorie et un success 
- Exemple: `curl http://127.0.0.1:5000/categories/1/questions`

``` 
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```

#### POST /questions
- General:
    - Cree une nouvelle question si le corps de la requete comprend question, answer, difficulty et category. Retourne l'id de la question crée et un success. 
    - S'il y'a un "searchTerm" dans le corps de la requete, cette renverra la liste des questions qui correspondent aux resultats de la recherche
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"How many days are in a week ?", "answer":"seven", "difficulty":5, "category":5}'`
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
EXAMPLE NEW QUESTION CREATED :
```
{
  "created (id)": 24,
  "success": true
}
```
EXAMPLE SEARCH :
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}

```
#### DELETE /questions/{question_id}
- General:
    - Supprime une question 
- `curl -X DELETE http://127.0.0.1:5000/questions/1`
```
{
  "deleted (id)": 24,
  "success": true
}
```
#### POST /quizzes
- General:
    - Cherche la prochaine question du quiz en se basant sur les questions deja vu et sur la categorie du quiz.
    la requete doit contenir : current_category (un objet contenant l'id et le type de la question) et previous_questions (une liste des id des questions vues)
- `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[17,16,18], "quiz_category":{"id": 2, "type": "test"}}' http://127.0.0.1:5000/quizzes`
```
{
  "question": {
    "answer": "Jackson Pollock",
    "category": 2,
    "difficulty": 2,
    "id": 19,
    "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
  },
  "success": true
}

```

## Auteur
Amadou DIALLO 


