from fastapi import APIRouter
import requests
import time
import os


# Sonarr API Endpoint and Header
SONARR_ENDPOINT = f"{SONARR_URL}/api/v3/series"
SONARR_HEADER = {"X-Api-Key": SONARR_API_KEY}

# Global variable to store the episode count
episode_count = 0

# Create a FastAPI router for Sonarr count
router = APIRouter()

# Function to update the episode count asynchronously
async def update_episode_count():
    global episode_count
    while True:
        try:
            series_response = requests.get(SONARR_ENDPOINT, headers=SONARR_HEADER)
            series_response.raise_for_status()
            series_list = series_response.json()

            total_episodes = 0
            for series in series_list:
                series_id = series["id"]
                episodes_response = requests.get(
                    f"{SONARR_URL}/api/v3/episode?seriesId={series_id}",
                    headers=SONARR_HEADER
                )
                episodes_response.raise_for_status()
                episodes = episodes_response.json()
                episodes_with_files = [episode for episode in episodes if episode.get("hasFile", False)]
                total_episodes += len(episodes_with_files)

            episode_count = total_episodes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching TV episodes: {e}")
        await asyncio.sleep(60)  # Asynchronous sleep for 1 minute

# Route to display the episode count
@router.get("/")
async def display_episode_count():
    if episode_count is None:
        return {"error": "Error fetching episode count"}
    return {"episode_count": episode_count}

# Route to display the episode count in a readable format
@router.get("/count")
async def display_count():
    if episode_count is None:
        return {"error": "Error fetching episode count"}
    return {"episode_count": episode_count}
