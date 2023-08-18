# Rent UAV backend project

### Tech Stack
- Python3
- Django
- Postgresql
- Rest Framework

# API DOCUMENTATION 

1. /api/v1/ - This is the base URL for the API version 1.

2. /api/v1/uav-categories/ - This endpoint is used to retrieve a list of UAV categories or create a new UAV category.

3. /api/v1/uav-categories/<int:pk>/ - This endpoint is used to retrieve, update, or delete a specific UAV category.

4. /api/v1/uavs/ - This endpoint is used to retrieve a list of UAVs or create a new UAV.

5. /api/v1/uavs/<int:pk>/ - This endpoint is used to retrieve, update, or delete a specific UAV.

6. /api/v1/rented-uavs/ - This endpoint is used to retrieve a list of rented UAVs or create a new rented UAV.

7. /api/v1/rented-uavs/<int:pk>/ - This endpoint is used to retrieve, update, or delete a specific rented UAV.

8. /api/v1/users/ - This endpoint is used to retrieve a list of users or create a new user.

9. /api/v1/users/<int:pk>/ - This endpoint is used to retrieve, update, or delete a specific user.

10. /api/v1/auth/token/ - This endpoint is used to obtain an authentication token by providing a valid username and password.

11. /api/v1/auth/token/refresh/ - This endpoint is used to refresh an existing authentication token by providing a valid refresh token.



# SETUP

1. Clone the repository
2. Create a virtual environment
3. Activate the virtual environment
4. Install the requirements
5. Create a .env file in the root directory of the project
6. Add the following environment variables to the .env file
    - SECRET_KEY
    - DEBUG
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
    - DB_HOST
    - DB_PORT
7. Run the migrations
8. Create a superuser
9. Run the server
10. Access the API endpoints
11. Run the tests
