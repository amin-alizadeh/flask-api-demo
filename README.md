# Flask REST API for Talent Adore
A basic API application built with Flask API.

## Features
* Minimal Flask 2.X App
* Unit tests
* Basic Type Hints
* App Structured Using Blueprints
* Application Factory Pattern Used
* Authentication Functionality Using JWT (Could be useful in JWT authentication of users across Microservices)
* Basic Database Functionality Included 
* Rate Limiting Functionality Based on Flask-Limiter For All The Routes In The Authentication Blueprint
* Support for .env and .flaskenv files build in


### Application Structure

The API is divided in blueprints `members`, `comments`, `users`, and `auth`.

The `comments` blueprint is responsible for handeling all requests related to comments, suchs as GET, POST and DELETE requests.

The `members` blueprint is responsible for handeling all requests related to members, suchs as GET, POST and DELETE requests.

The `users` blueprint handles the user related requests. Currently there are two routes which return either information ahout the current user or a different user based on username.

The `auth` blueprint is responsible for all the routes associated with user registration and authentication.


## Installation

### Virtual Environment Setup

It is preferred to create a virtual environment per project, rather then installing all dependencies of each of your 
projects system wide. Once you install [virtual env](https://virtualenv.pypa.io/en/stable/installation/), and move to 
your projects directory through your terminal, you can set up a virtual env with:

```bash
python3 -m venv .venv
```

### Dependency installations

To install the necessary packages:

```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

This will install the required packages within your venv.

---

## Environment Variables

1. `SQLALCHEMY_DATABASE_URI` contains the full URL string to connect to the database. You can also inject username, password, and the connection URL using other secret handling tools depending on the environment to the as variables and construct the URI accordingly. For testing purposes, the username and password are provided as clear text here.
1. `API_KEY_SECRET` is injected as an environment variable using variety of technics compliant with security protocols and best practices as environment variables.
1. Other envrionment variables are for additional security when needed. The uses for them are not implemented in this test.


### Setting up the Database

Database migrations are handled through Flask's Migrate Package, which provides a wrapper around Alembic. Migrations are done for updating and creating necessary tables/entries in your database. Flask provides a neat way of handling these. The files generate by the migrations should be added to source control.

To setup a SQLite3 database for development (SQLite3 is **not** recommended for production, use something like PostgreSQL or MySQL) you navigate to the folder where `flask_api.py` is located and run:

```bash
export FLASK_APP=flask_api.py
```

then you need to initiate your database and the migration folder with the following commands:

```bash
flask db init
```

```bash
flask db migrate "Your message here"
```

```bash
flask db upgrade
```

### Migrations

To make changes to the database structure you can also use the `flask db` commands:

```bash
export FLASK_APP=flask_api.py
```

```bash
flask db migrate -m "Your message here"
```

```bash
flask db upgrade
```

---

## Running the Application

Once you have setup your database, you are ready to run the application.
Assuming that you have exported your app's path by:

```bash
export FLASK_APP=flask_api.py
```

You can go ahead and run the application with a simple command:

```bash
flask run
```



# Docker and Composer
A docker has been included in this project.

```bash
docker build -t ta-flask . 
```

And to run the docker

```bash
docker run -p 8000:8000 ta-flask  
```

## Acknowledgements
[Flask API Template](https://github.com/StefanVDWeide/flask-api-template)
