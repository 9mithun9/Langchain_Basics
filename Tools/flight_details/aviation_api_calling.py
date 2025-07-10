from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()


@tool
def get_flights(departure: str, arrival: str, limit: int)-> list:
    """Fetches the limit no of flight information between two airports 'departure' and 'arrival' using their IATA codes."""
     
    api_key = os.getenv("AVIATIONSTACK_API_KEY")
    if not api_key:
        return {"error": "API key not loaded. Check your .env file and load_dotenv()."}

    
    url = f'http://api.aviationstack.com/v1/flights'
    params = {
        "access_key": api_key,
        "dep_iata": departure,
        "arr_iata": arrival,
        "limit": limit
    }
    response = requests.get(url, params)
    result = response.json()
    if "data" not in result:
        return [{"error": "No flight data found."}]

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

#print(get_flights.invoke({'departure': 'DXB', 'arrival': 'LHR'}))


model = ChatOpenAI( 
    model = "gpt-4o"
)

binded_model = model.bind_tools([get_flights])

message_history = []
query = HumanMessage("What are the 5 flight information between departure airport 'DXB' and arrival airport 'LHR'?")
message_history.append(query)

ai_message = binded_model.invoke(message_history)

message_history.append(ai_message)


tool_message = get_flights.invoke(ai_message.tool_calls[0])
message_history.append(tool_message)

result = binded_model.invoke(message_history)
print(result)
