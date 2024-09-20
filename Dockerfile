FROM python:3.12-slim-bullseye

RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install Poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copy your FastAPI application
COPY app.py ./
COPY src ./

# Set the working directory
WORKDIR /app

# Command to run your FastAPI application
CMD ["poetry", "run", "uvicorn", "app:app", "--reload"]