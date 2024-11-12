# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the Poetry files (pyproject.toml and poetry.lock) into the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install the project dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the project files into the container
COPY . /app/

# Set the entrypoint (replace "your_script.py" with your main Python script)
CMD ["poetry", "run", "default"]




