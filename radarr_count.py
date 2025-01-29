from fastapi import APIRouter
import requests
import os
import asyncio


# Radarr API Endpoint and Header
RADARR_ENDPOINT = f"{RADARR_URL}/api/v3/movie"
RADARR_HEADER = {"X-Api-Key": RADARR_API_KEY}

# Global variable to store the movie count
movie_count = 0

# Create a FastAPI router
router = APIRouter()

# Function to update movie count asynchronously
async def update_movie_count():
    global movie_count
    while True:
        try:
            response = requests.get(RADARR_ENDPOINT, headers=RADARR_HEADER)
            response.raise_for_status()
            movies = response.json()
            movies_with_files = [movie for movie in movies if movie.get("hasFile", False)]
            movie_count = len(movies_with_files)
            print(f"Updated movie count: {movie_count}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Movies: {e}")
        await asyncio.sleep(60)  # Wait 60 seconds before checking again

# Route to display the movie count
@router.get("/")
async def display_movie_count():
    if movie_count is None:
        return {"error": "Error fetching movie count"}
    return {"movie_count": movie_count}

# Start the background task for updating the movie count
async def start_movie_count_update():
    await update_movie_count()

