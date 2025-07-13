# Twitter-like Web App

A simple web application that allows users to create and view posts, similar to Twitter.

## Features

- Create posts with username and content
- View all posts in chronological order
- Modern UI using Tailwind CSS
- SQLite database for data persistence

## Setup

1. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter your username
2. Write your post in the text area
3. Click "Post" to submit
4. Your post will appear in the feed below

## Technologies Used

- Flask (Python web framework)
- SQLAlchemy (Database ORM)
- Tailwind CSS (Styling)
- SQLite (Database)
