# Django REST Framework Boilerplate

![Django](https://img.shields.io/badge/Django-3.2-blue)
![Python](https://img.shields.io/badge/Python-3.8+-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

This project provides a starting point for building RESTful web services using the Django REST Framework. It demonstrates how to set up a basic API structure and serves as a skeleton for new projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Compatible with **Django 3.2** and **Python 3.8+**
- Integrated with Django REST Framework
- User authentication and authorization (with JWT support)
- Basic CRUD operations for API endpoints
- Blog and Category management endpoints
- PostgreSQL database integration
- Containerized setup with Docker
- API documentation with Swagger UI

## Installation

### Requirements

- Python 3.8 or higher
- PostgreSQL
- Docker and Docker Compose (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/cemre-2187/django-rest-framework-boilerplate.git
cd django-rest-framework-boilerplate
```

### Step 2: Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the `.env.example` file to `.env` and update the necessary variables.

```bash
cp .env.example .env
```

### Step 5: Prepare the Database

```bash
python manage.py migrate
```

### Step 6: Start the Development Server

```bash
python manage.py runserver
```

### Using Docker (Optional)

If you prefer to use Docker, you can run the application in a container with the following commands:

```bash
docker-compose up --build
```

## Usage

Once the API server is running, the following endpoints will be available:

### Account Management

- **`/api/account/register/`**: Register a new user.
- **`/api/account/login/`**: Log in an existing user.

### Blog Management

- **`/api/blog/`**: List blog posts and add new posts.
- **`/api/blog/category/`**: List categories and add new categories.
- **`/api/blog/stats/`**: View blog statistics.

## API Documentation

You can access the API documentation through Swagger UI. After starting the development server, go to `http://localhost:8000/swagger/`.

## Project Structure

```plaintext
django-rest-framework-boilerplate/
│
├── api/
│   ├── account/
│   │   ├── urls.py
│   │   └── views.py
│   ├── blog/
│   │   ├── urls.py
│   │   └── views.py
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── urls.py
│
├── manage.py
├── requirements.txt
└── docker-compose.yml
```

- **core/**: Main project settings and configurations.
- **apps/account/**: Handles user registration and login.
- **apps/blog/**: Manages blog posts and categories.
- **api/urls.py**: General API routing.
- **manage.py**: Script for running Django management commands.
- **docker-compose.yml**: Docker configuration file.

## Contributing

We welcome contributions! If you want to work on this project, please open an [issue](https://github.com/cemre-2187/django-rest-framework-boilerplate/issues) or send a pull request.

1. Fork this repository.
2. Create a new feature branch (`git checkout -b new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to your branch (`git push origin new-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

This README file now provides detailed information about the project, including the account and blog applications and their URL configurations. You can further update it as needed for more specific details.