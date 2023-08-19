# Rent UAV backend project

### Tech Stack
- Python3
- Django
- Postgresql
- Rest Framework

# API DOCUMENTATION 

You can click this link for api endpoints.
- http://0.0.0.0:8000/swagger/

# RUN WITH DOCKER
- docker-compose up
- docker-compose exec web python manage.py createsuperuser


# SETUP

1. Clone the repository
2. Create a virtual environment
3. Activate the virtual environment
4. Install the requirements
5. Create a .env file in the root directory of the project
6. Add the following environment variables to the .env file
    - DEBUG
    - SECRET_KEY 
    - PG_DB_HOST
    - PG_DB_USER
    - PG_DB_PASSWORD
    - PG_DB_NAME
    - PG_DB_PORT
7. Run the migrations
8. Create a superuser
9. Run the server
10. Access the API endpoints
11. Run the tests
