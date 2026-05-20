# Book Library - Book Recommendation System

A modern Flask application with a dark, high-contrast UI design and content-based recommendation engine.

## Features
- **Modern Dark UI**: High-contrast design with cyan accent colors, superior typography, and smooth animations.
- **Smart Recommendations**: Jaccard similarity-based book suggestions.
- **User Features**: Authentication, Watchlist, Reviews, Ratings.
- **Cart & e-Commerce**: Add books to cart, purchase, and download PDFs.
- **Admin Dashboard**: Full CRUD for books, user management, and analytics.
- **Search**: Instant search by title, author, or genre.
- **Security**: Role-based access control (Admin/User).

## Prerequisites
1. **Python 3.8+** installed and added to System PATH.
2. **MySQL Server** running locally.
3. **Git** (optional).

## Installation

1. **Clone/Download** the repository.
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Open `config.py` and update `SQLALCHEMY_DATABASE_URI` if your MySQL credentials differ from `root:password`.
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost/bookrecommendation_db'
   ```
2. (Optional) Add Stripe keys to `config.py` or `.env` for payments.

## Database Setup & Seeding

1. **Initialize and Seed Data**:
   Run the included script to create tables and generate sample books, users, and reviews.
   ```bash
   python scripts/seed_data.py
   ```
   *Note: This script drops existing tables to start fresh.*

2. **Import Real Data (Optional)**:
   Download [Goodreads Books](https://www.kaggle.com/jealousleopard/goodreadsbooks) CSV.
   ```bash
   python scripts/import_csv.py path/to/books.csv
   ```

## Running the App

### Option 1: Using the Startup Script (Windows)
Just double-click `run_app.bat` or run it in your terminal:
```batch
.\run_app.bat
```

### Option 2: Manual Start
1. **Activate the Virtual Environment**:
   ```bash
   .\venv\Scripts\activate
   ```
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your browser to `http://127.0.0.1:5000`.

## Default Accounts
- **Admin**: `admin@example.com` / `password`
- **User**: `user0@example.com` / `password`

## Design System

The application uses a dark, high-contrast design system with:
- **Primary Background**: Deep black (#0a0a0a)
- **Accent Color**: Vibrant cyan (#00d4ff)
- **Typography**: Inter for UI, Outfit for headings
- **Components**: Glass panels, gradient buttons, smooth transitions
