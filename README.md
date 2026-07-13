## Introduction

This project is a Django web application for a digital marketplace platform. It includes a database and runs inside Docker containers using Docker Compose. This document provides instructions on how to install, set up, run, and use this Docker container with the Django website.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the Repository:**

```shell script
git clone https://github.com/goetic-zoe/UFCFTR-30-3-Distributed-and-Enterprise-Software-Development.git
cd bristol_regional_food_network
```


2. **Build the Docker Images:**

```shell script
docker compose build
```


3. **First time run the Containers:**

```shell script
docker compose up
docker compose down
```
After first run after build it is recommended to restart the container due to a chance of it preemptively attempting to connect to the database while it is still building.


4. **Create and Apply Database Migrations:**

```shell script
docker compose up -d
docker compose exec web python manage.py migrate
```


5. **Create a Superuser (Optional but recommended for admin access):**

```shell script
docker compose exec web python manage.py createsuperuser
```


## Running the Application

- **Start the Containers:**

```shell script
docker compose up -d
```


- **Stop the Containers:**

```shell script
docker compose down
```


- **View Logs:**

```shell script
docker compose logs -f web
```

- **Run Tests:**
```shell script
docker compose exec web python manage.py test
```

## Usage

### Accessing the Application

Once the containers are running, you can access the Django application via your web browser:

- Open a web browser and navigate to [http://localhost:8000](http://localhost:8000).

### Admin Panel

To access the Django admin panel, use the superuser credentials created earlier:

- Navigate to [http://localhost:8000/admin](http://localhost:8000/admin) and log in with your superuser credentials.

### Database Access

The MySQL database is accessible through Docker Compose. You can connect to it using any MySQL client:

```shell script
docker compose exec db mysql -udjango_user -pdjango_pass bristol_food_network
```


## Development

### Running Django Shell

To run the Django shell inside the container:

```shell script
docker compose exec web python manage.py shell
```


### Collecting Static Files

If you make changes to static files or add new ones, collect them using:

```shell script
docker compose exec web python manage.py collectstatic --noinput
```


## Directory Structure

- **bristol_regional_food_network/**
  - **digital_marketplace_platform/**: Django app directory containing models, views, templates, etc.
  - **static/**: Static files for the application (CSS, JavaScript, images).
  - **templates/**: HTML templates for the application.
  - **manage.py**: Command-line utility for administrative tasks.
  - **settings.py**: Configuration settings for Django.
  - **urls.py**: URL declarations for the project.
- **compose.yaml**: Docker Compose configuration file.
- **Dockerfile**: Instructions for building the Docker image.
- **requirements.txt**: List of Python dependencies.

## Additional Notes

- Ensure that Docker and Docker Compose are installed and running on your machine.
- The database is stored in a named volume (`db_data`) to persist data between container restarts.
- The application runs on port 8000, which is exposed by the `web` service in Docker Compose.

For further assistance or customization, refer to the Django documentation and Docker Compose guides.
