FROM python:slim-bookworm

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject and lock file
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]