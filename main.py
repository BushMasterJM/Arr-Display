from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
from typing import Optional
import asyncio
from threading import Thread

# Load .env file
load_dotenv()

# Load configuration from .env file
RADARR_API_KEY = os.getenv("RADARR_API_KEY")
RADARR_URL = os.getenv("RADARR_URL")
SONARR_API_KEY = os.getenv("SONARR_API_KEY")
SONARR_URL = os.getenv("SONARR_URL")

# Toggle scripts on/off
ENABLE_RADARR_COUNT_SCRIPT = os.getenv("ENABLE_RADARR_COUNT_SCRIPT") == "True"
ENABLE_SONARR_COUNT_SCRIPT = os.getenv("ENABLE_SONARR_COUNT_SCRIPT") == "True"
ENABLE_RADARR_POSTER_SCRIPT = os.getenv("ENABLE_RADARR_POSTER_SCRIPT") == "True"
ENABLE_SONARR_POSTER_SCRIPT = os.getenv("ENABLE_SONARR_POSTER_SCRIPT") == "True"

# Create FastAPI apps for each script
radarr_count_app = FastAPI()
sonarr_count_app = FastAPI()
radarr_poster_app = FastAPI()
sonarr_poster_app = FastAPI()

# Run Radarr count script if enabled
if ENABLE_RADARR_COUNT_SCRIPT:
    print("Starting Radarr count script...")

    @radarr_count_app.get("/")
    async def display_movie_count():
        # Placeholder logic for Radarr count, replace with actual logic
        return {"message": "Radarr movie count here"}

# Run Sonarr count script if enabled
if ENABLE_SONARR_COUNT_SCRIPT:
    print("Starting Sonarr count script...")

    @sonarr_count_app.get("/")
    async def display_episode_count():
        # Placeholder logic for Sonarr count, replace with actual logic
        return {"message": "Sonarr episode count here"}

# Run Radarr poster script if enabled
if ENABLE_RADARR_POSTER_SCRIPT:
    print("Starting Radarr poster script...")

    @radarr_poster_app.get("/poster")
    async def display_radarr_poster():
        # Placeholder logic for Radarr poster, replace with actual logic
        return {"message": "Radarr poster here"}

# Run Sonarr poster script if enabled
if ENABLE_SONARR_POSTER_SCRIPT:
    print("Starting Sonarr poster script...")

    @sonarr_poster_app.get("/poster")
    async def display_sonarr_poster():
        # Placeholder logic for Sonarr poster, replace with actual logic
        return {"message": "Sonarr poster here"}

# Run each FastAPI app on its own port using uvicorn
def run_uvicorn(app, port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Create separate threads to run each app concurrently
    threads = []

    if ENABLE_RADARR_COUNT_SCRIPT:
        thread = Thread(target=run_uvicorn, args=(radarr_count_app, 6901))
        threads.append(thread)
    
    if ENABLE_SONARR_COUNT_SCRIPT:
        thread = Thread(target=run_uvicorn, args=(sonarr_count_app, 6902))
        threads.append(thread)

    if ENABLE_RADARR_POSTER_SCRIPT:
        thread = Thread(target=run_uvicorn, args=(radarr_poster_app, 6903))
        threads.append(thread)

    if ENABLE_SONARR_POSTER_SCRIPT:
        thread = Thread(target=run_uvicorn, args=(sonarr_poster_app, 6904))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Join the threads to keep them running
    for thread in threads:
        thread.join()
