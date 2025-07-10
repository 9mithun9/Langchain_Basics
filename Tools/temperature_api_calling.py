from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, InjectedToolArg
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
from typing import Annotated
import requests

load_dotenv()

@tool
def get_weather(lat: float, long: float) -> float:
    """Finds out the weather of a particular place given it's latitude and longitude as lat and long"""
    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true'
    response = requests.get(url)
    return response.json()['current_weather']['temperature']

@tool 
def convert_weather(temp: Annotated[float, InjectedToolArg]) -> float:
    """Converts any temperature as temp to Farenheit"""
    return round((((9/5) * temp) + 32),2)


query = HumanMessage('What is the temperature of latitude 13.447059 and longitude 101.543826? After that convert that temperature to Farenheit.')

message_history = [query]

model = ChatOpenAI(
    model = "gpt-4o"
)

binded_model = model.bind_tools([get_weather, convert_weather])
ai_message = binded_model.invoke(query.content)
message_history.append(ai_message)


for tool_call in ai_message.tool_calls:
    #print(tool_call)
    if tool_call['name'] == 'get_weather':
        temp_cel = get_weather.invoke(tool_call).content
        message_history.append(get_weather.invoke(tool_call))
    if tool_call['name'] == 'convert_weather':
        tool_call['args']['temp'] = temp_cel
        result = convert_weather.invoke(tool_call)
        message_history.append(result)
        #print(result)

#print(message_history)

print(binded_model.invoke(message_history).content)

