
# base image
FROM python:3.9-slim-buster

# set working directory
WORKDIR /app

# copy the requirements file into the container
COPY requirements.txt .

# install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    pip install --no-cache-dir -r requirements.txt

# copy the application code into the container
COPY . .

# expose port 5000 for the Flask app
EXPOSE 5000


ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db/${DB_NAME}

# start the application
CMD ["flask", "run", "--host", "0.0.0.0"]
