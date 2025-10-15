# 🎬 Movie Web Application — Django RESTful API

A RESTful web service built with **Django** and **Django REST Framework (DRF)** for managing movies and their metadata.  
This project demonstrates end-to-end data management, including CRUD operations, data preprocessing, normalization, and testing for a clean, scalable movie database.

---

## 🧩 Overview

The **Movie Web Application** provides API endpoints for creating, reading, updating, and deleting movie data, including related genres, stars, and directors.  
It uses a relational database schema normalized up to **Third Normal Form (3NF)** to ensure data integrity and minimal redundancy.  

The system also supports bulk data import from cleaned CSV files and includes comprehensive unit testing to validate reliability and performance.

---

## 🧠 Key Features

| Feature | Description |
|----------|-------------|
| **CRUD Operations** | Create, update, and delete movie entries through RESTful API endpoints. |
| **User Roles** | Supports admin and customer roles for different access levels. |
| **Data Preprocessing** | Cleans and standardizes data for runtime, votes, ratings, and text fields. |
| **Bulk Data Loading** | Automated CSV import using Django ORM for Movies, Genres, Stars, and Directors. |
| **REST Endpoints** | Implements pagination, filtering by genre, and top-rated movie retrieval. |
| **Normalization** | Ensures 1NF, 2NF, and 3NF compliance for optimal data integrity. |
| **Unit Testing** | Covers models, endpoints, authentication, and data import scripts. |

---

## 🧮 Database Schema

**Models:**
- `User`: Username, Email, Role, Is_Admin, Is_Active  
- `Movie`: Title, Runtime, Certificate, Rating, Description, Votes  
- `Genre`: Foreign key → Movie  
- `Star`: Foreign key → Movie  
- `Director`: Foreign key → Movie  

**Relationships:**  
- One-to-many: A movie can have multiple genres, stars, and directors.  

---

## 🔗 REST Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/admin-dashboard/` | GET | Admin interface for movie management |
| `/customer-dashboard/` | GET | Displays user-accessible movie listings |
| `/top-movies/` | GET | Shows top 5 highest-rated movies |
| `/view-movies/` | GET | Lists movies with genre-based filtering |
| `/update/<id>/` | PUT | Updates existing movie data |
| `/delete/<id>/` | DELETE | Removes movie record |

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/movie-webapp.git
cd movie-webapp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run database migrations
python manage.py migrate

# 4. Load dataset
python populate_movies.py

# 5. Start server
python manage.py runserver
