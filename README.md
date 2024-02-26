Authentication form is rendered at http://localhost:5000/. <br/>
If successfully authenticated, profile page is rendered at http://localhost:5000/profile. <br/> 
If no authentication, user cannot reach profile page. <br/>
Username and password are stored in PostgreSQL (connection with psycopg2 + peewee) <br/>
