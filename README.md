Authentication form is rendered at http://localhost:5000/.
If successfully authenticated, profile page is rendered at http://localhost:5000/profile. 
If no authentication, user cannot reacg profile page.
Username and password are stored in PostgreSQL (connection with psycopg2 + peewee)
