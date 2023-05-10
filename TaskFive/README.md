## Web application for weather forcast in different cities
### The app uses Flask Framework.
### It create DB with Flask-SQLAlchemy and flask-migrate
### It has two options with entering the city:                                                                                         
   * get data - takes information live from API
   * refresh - takes information from Postgres DB                                                                                           
### The app and DB are in Docker container:                                                                                
  * using Dockerfile and docker-compose file
