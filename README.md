# Project Setup

This project requires the creation of two PostgreSQL databases: a main database and a test database. 
Below are the steps to configure and set up the environment.

# Prerequisites
Ensure you have the following installed:

- Docker and Docker Compose\n
- PostgreSQL
- Redis

# Environment Variables

Set up the following environment variables in a .env file:

# CELERY
BROKER="redis://redis:6379/0"

# DATABASE
DATABASE_URL="postgresql+asyncpg://postgres:postgres@db:5432/test_work_25"
DB_NAME=test_work_25
DB_USER=postgres
DB_PASSWORD=postgres

# TEST DATABASE
TEST_DATABASE_URL="postgresql+asyncpg://postgres:postgres@test_db:5432/test_db"
TEST_DB_NAME=test_db
TEST_DB_USER=postgres
TEST_DB_PASSWORD=postgres
