# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize FastAPI app
app = FastAPI()

# Define request model for trip planner
class TripPlannerRequest(BaseModel):
    where_to: str
    number_of_days: int
    itinerary_type: str
    when_your_trip_start: str
    travel_preference: str
    budget: int

# Endpoint to handle trip planner requests
@app.post("/trip_planner_api")
def trip_planner(request: TripPlannerRequest):
    # Use the GEMINI_API_KEY to authenticate with the Gemini API
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Prepare the payload for the API request
    payload = {
        "where_to": request.where_to,
        "number_of_days": request.number_of_days,
        "itinerary_type": request.itinerary_type,
        "when_your_trip_start": request.when_your_trip_start,
        "travel_preference": request.travel_preference,
        "budget": request.budget
    }

    # Make a request to the Gemini API (update the URL according to the Gemini API documentation)
    response = requests.post('https://api.gemini.com/v1/some-endpoint', headers=headers, json=payload)

    # Handle the response from the Gemini API
    if response.status_code == 200:
        return {"success": True, "response": response.json()}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
