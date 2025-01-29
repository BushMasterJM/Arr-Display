# Start from a base Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files into the container
COPY . /app/

# Expose the necessary ports
EXPOSE 6901 6902 6903 6904

# Set the entry point to run the FastAPI app
CMD ["uvicorn", "main:radarr_app", "--host", "0.0.0.0", "--port", "6901", "--reload"]
