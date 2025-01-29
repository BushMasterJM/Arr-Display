from fastapi import APIRouter
import requests
import os
import random
from urllib.request import urlretrieve
import time

# Radarr API Endpoint and Header
RADARR_ENDPOINT = f"{RADARR_URL}/api/v3/movie"
RADARR_HEADER = {"X-Api-Key": RADARR_API_KEY}

# Global variables
current_poster = None
poster_file_path = "assets/radarr_poster.jpg"

# Create a FastAPI router
router = APIRouter()

# Function to fetch and update the poster asynchronously
async def fetch_and_update_poster():
    global current_poster

    while True:
        try:
            # Fetch all movies
            response = requests.get(RADARR_ENDPOINT, headers=RADARR_HEADER)
            response.raise_for_status()
            movies = response.json()

            # Select a random movie with a poster
            posters = []
            for movie in movies:
                for image in movie.get("images", []):
                    if image.get("coverType") == "poster":
                        posters.append({"title": movie["title"], "url": f"{RADARR_URL}{image['url']}"})

            if posters:
                random_poster = random.choice(posters)
                current_poster = random_poster["url"]

                # Download the poster
                urlretrieve(random_poster["url"], poster_file_path)
                print(f"Updated poster: {random_poster['title']}")

                # Wait for 1 minute before updating again
                await asyncio.sleep(60)  # Asynchronous sleep for 1 minute

                # Delete the poster file
                if os.path.exists(poster_file_path):
                    os.remove(poster_file_path)
                    print("Poster file deleted.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies: {e}")
            await asyncio.sleep(60)  # Retry after 1 minute

# Route to display the poster
@router.get("/")
async def display_poster():
    if os.path.exists(poster_file_path):
        # Return the current poster
        return {"poster_url": "/assets/radarr_poster.jpg"}
    else:
        return {"error": "No poster available"}

# Route to serve the poster file
@router.get("/assets/radarr_poster.jpg")
async def serve_poster():
    if os.path.exists(poster_file_path):
        return {"poster_url": "/assets/radarr_poster.jpg"}
    else:
        return {"error": "No poster available"}
