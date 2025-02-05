version: '3.8'

services:
  web:
    build:
      context: . 
      dockerfile: docker/Dockerfile
    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app  
    ports:
      - "8000:8000" 
    environment:
      - DEBUG=False
      - DJANGO_SETTINGS_MODULE=core.settings.prod  # Reference to your production settings
      - SECRET_KEY=your_secret_key  # You can generate a secure key
      - DB_NAME=django_prod
      - DB_USER=django_user
      - DB_PASSWORD=your_db_password
      - DB_HOST=db  # Link it to the database service
      - DB_PORT=5432
    depends_on:
      - db  # Ensure the db service is started before the Django app

  db:
    image: postgres:13-alpine  # Using PostgreSQL image
    environment:
      - POSTGRES_DB=django_prod
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=your_db_password
    volumes:
      - db_data:/var/lib/postgresql/data  # Persist data even after container restart
    ports:
      - "5432:5432"

volumes:
  db_data:  # Named volume for PostgreSQL data persistence
