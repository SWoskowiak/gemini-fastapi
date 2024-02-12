# About this project

This is a simple demo project to test out htmx/fastapi as well as gemini-vision-pro with a smattering of cloud storage usage and very basic tests.

This is just a POC to play around w/ Python and AI and to explore HTMX and how usable it is. This is not a "production ready" app but merely an exploratory exercise!

## Startup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/SWoskowiak/gemini-fastapi.git
```

## 2. Install Docker

This project uses Docker to run a PostgreSQL instance. If you don't have Docker installed, download it from the [official Docker website](https://www.docker.com/products/docker-desktop).

## 3. Start the PostgreSQL Instance

Run the following command to start a PostgreSQL instance using Docker:

```bash
docker run -d --name gemini-test-app --restart unless-stopped -e POSTGRES_USER=gemini-user -e POSTGRES_DB=gemini-db -e POSTGRES_PASSWORD="secretPassword" -p 32768:5432 postgres:14.10
```

Remember to replace `"secretPassword"` with a secure password.

## 4. Install Dependencies

This project uses Poetry for dependency management. If you don't have Poetry installed, install it following the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

Once installed, at the project root you can install all the project dependencies using:

```bash
poetry install
```

## 5. Set Up Environment Variables

Create a `.env` file at the root of the project and define the following variables:

- `DB_URL`: The SQLAlchemy compatible connection string for your PostgreSQL instance. It should look like this: `"postgresql://gemini-user:secretPassword@localhost:32768/gemini-db"`. Replace `"secretPassword"` with the password you used in step 3.
- `GOOGLE_GEMINI_API_KEY`: Your API key for the `gemini-vision-pro` model.
- `USE_CLOUD_STORAGE`: Set this to `TRUE` if you want to use Google Cloud Storage for storing images. If this is `FALSE`, images will not be stored.
- `BUCKET_NAME`: The name of your Google Cloud bucket. This is only needed if `USE_CLOUD_STORAGE` is `TRUE`.
- `GOOGLE_APPLICATION_CREDENTIALS`: The path to the key for your service account for the project your bucket lives under. This is only needed if `USE_CLOUD_STORAGE` is `TRUE`.

## 6. Enter the Poetry Shell

Before running Alembic and Uvicorn, you should enter the Poetry shell. This will ensure that you're using the virtual environment created by Poetry, which has all the project dependencies installed. You can enter the Poetry shell with the following command:

```bash
poetry shell
```

## 7. Run Migrations

Use Alembic to run database migrations with the following command:

```bash
alembic upgrade head
```

## 8. Run Tests

Use Pytest to run our test files

```bash
pytest
```

## 9. Start the Application

Finally, start the application using Uvicorn with the following command:

```bash
uvicorn main:app --reload
```
