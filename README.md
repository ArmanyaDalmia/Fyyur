# Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Overview

This app is capable of doing the following using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

## Tech Stack

The tech stack includes:

* **SQLAlchemy ORM** as the ORM library of choice
* **PostgreSQL** as the database of choice
* **Python3** and **Flask** as the server language and server framework respectively
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend

## Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask).

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

## Authors

I primarily worked on the `app.py`, `config.py`, and `forms.py` files in order to build the data models and API endpoints used by the web app. I also worked on the files in the `forms` subdirectory in the `templates` directory and on this README based off of the provided material. All other project files including the frontend were provided by Udacity as a project in the Full Stack Web Developer Nanodegree course. 

## Acknowledgements

The Udacity Full Stack Nanodegree Instructor and Course developers

