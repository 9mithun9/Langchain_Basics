from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests
import os

load_dotenv()

app = FastAPI()


@tool
def get_flights(departure: str, arrival: str, limit: int) -> list:
    """
    Fetches up to `limit` number of flight results between two IATA airport codes.
    Returns simplified flight info.
    """
    api_key = os.getenv("AVIATIONSTACK_API_KEY")
    if not api_key:
        return [{"error": "API key not loaded. Check your .env file."}]

    # Enforce limit max to 5
    if limit > 5:
        limit = 5

    url = "http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": api_key,
        "dep_iata": departure,
        "arr_iata": arrival,
        "limit": limit
    }

    response = requests.get(url, params=params)
    result = response.json()

    if "data" not in result or not result["data"]:
        return [{"error": f"No valid flights found. Please check the IATA codes: '{departure}' and '{arrival}'."}]

    cleaned_flights = []
    for flight in result["data"]:
        cleaned_flights.append({
            "flight_date": flight.get("flight_date"),
            "flight_status": flight.get("flight_status"),
            "airline": flight.get("airline", {}).get("name"),
            "flight_number": flight.get("flight", {}).get("number"),
            "departure_time": flight.get("departure", {}).get("scheduled"),
            "arrival_time": flight.get("arrival", {}).get("scheduled")
        })

    return cleaned_flights


class FlightQuery(BaseModel):
    departure: str = Field(..., min_length=3, max_length=3)
    arrival: str = Field(..., min_length=3, max_length=3)
    limit: int = Field(..., ge=1, le=5)  # Max allowed: 5


@app.post("/flights")
def fetch_flight_info(query: FlightQuery):
    return {"flights": get_flights.invoke(query.dict())}
