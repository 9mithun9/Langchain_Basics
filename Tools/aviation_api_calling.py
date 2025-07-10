from langchain_core.tools import tool
import json
import requests

@tool
def get_flights(departure: str, arrival: str)-> json:
    """Fetches the latest flight information between two airports 'departure' and 'arrival' using their IATA codes."""
     
    url = f'http://api.aviationstack.com/v1/flights'
    params = {
        "access_key": "cef2350c2400769639b4761cce8357ad",  
        "dep_iata": departure,
        "arr_iata": arrival,
        "limit": 1
    }
    response = requests.get(url, params)
    return response.json()

print(get_flights.invoke({'departure': 'DXB', 'arrival': 'LHR'})['data'])
