from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import asyncio, os, time
from dotenv import load_dotenv
from pydantic import BaseModel

class TravelResponse(BaseModel):
    weather_info: str
    flight_info: str
    hotel_info: str
    summary: str

load_dotenv()

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

# Multiple tools that can be called in parallel
async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    # Simulate API delay
    await asyncio.sleep(1)
    return f"Weather in {city}: 75°F, sunny with light clouds. Perfect for sightseeing!"

async def get_flight_info(departure_city: str, destination_city: str) -> str:
    """Get flight information between two cities."""
    # Simulate API delay
    await asyncio.sleep(1.5)
    return f"Flights from {departure_city} to {destination_city}: Multiple options available. Best price: $350, Duration: 3h 45m"

async def get_hotel_info(city: str) -> str:
    """Get hotel information for a city."""
    # Simulate API delay
    await asyncio.sleep(1.2)
    return f"Hotels in {city}: 5-star hotels available from $180/night. 4-star options from $120/night"

async def get_local_attractions(city: str) -> str:
    """Get local attractions and activities for a city."""
    # Simulate API delay
    await asyncio.sleep(0.8)
    return f"Top attractions in {city}: Historic downtown, art museums, local food tours, and scenic parks"

async def get_restaurant_recommendations(city: str) -> str:
    """Get restaurant recommendations for a city."""
    # Simulate API delay
    await asyncio.sleep(1.1)
    return f"Best restaurants in {city}: Italian bistro (4.8★), Local steakhouse (4.6★), Farm-to-table cafe (4.7★)"

# Create strict function tools for parallel execution
weather_tool = FunctionTool(get_weather, description="Get weather information for a city", strict=True)
flight_tool = FunctionTool(get_flight_info, description="Get flight information between cities", strict=True)
hotel_tool = FunctionTool(get_hotel_info, description="Get hotel information for a city", strict=True)
attractions_tool = FunctionTool(get_local_attractions, description="Get local attractions for a city", strict=True)
restaurant_tool = FunctionTool(get_restaurant_recommendations, description="Get restaurant recommendations for a city", strict=True)

# Agent with multiple tools for parallel execution
travel_agent = AssistantAgent(
    name="travel_agent",
    model_client=az_model_client,
    tools=[weather_tool, flight_tool, hotel_tool, attractions_tool, restaurant_tool],
    system_message="""You are a helpful travel planning assistant. When asked about travel plans, 
    you should gather comprehensive information by calling multiple tools in parallel to provide 
    complete travel recommendations. Always try to get weather, flights, hotels, attractions, 
    and restaurant information when planning a trip.""",
    reflect_on_tool_use=True,
    model_client_stream=False,
)

async def demonstrate_parallel_tools():
    """Demonstrate parallel tool calls with timing."""
    
    print("=== Parallel Tool Calls Demo ===\n")
    
    # Task that will trigger multiple tool calls
    task = """I'm planning a trip from New York to San Francisco. 
    Can you help me get comprehensive travel information including weather, 
    flights, hotels, attractions, and restaurants?"""
    
    print(f"Task: {task}\n")
    print("Starting travel planning (this will call multiple tools in parallel)...\n")
    
    start_time = time.time()
    
    # The agent will automatically determine which tools to call and can execute them in parallel
    response = await travel_agent.run(task=task)
    
    end_time = time.time()
    
    print("=== RESPONSE ===")
    print(response)
    print(f"\n=== EXECUTION TIME: {end_time - start_time:.2f} seconds ===")
    print("\nNote: If tools were called sequentially, this would take much longer!")
    print("The agent automatically determined which tools to call and executed them efficiently.")

async def demonstrate_streaming_with_parallel_tools():
    """Demonstrate parallel tool calls with streaming."""
    
    print("\n\n=== Streaming Parallel Tool Calls Demo ===\n")
    
    task = """Plan a weekend getaway to Miami. I need weather forecast, 
    hotel options, local attractions, and restaurant recommendations."""
    
    print(f"Task: {task}\n")
    print("Streaming response with parallel tool execution:\n")
    
    # Enable streaming to see tool calls happen in real-time
    travel_agent_streaming = AssistantAgent(
        name="travel_agent_streaming",
        model_client=az_model_client,
        tools=[weather_tool, hotel_tool, attractions_tool, restaurant_tool],
        system_message="""You are a helpful travel planning assistant. Gather comprehensive 
        information by calling multiple tools in parallel when planning trips.""",
        reflect_on_tool_use=True,
        model_client_stream=True,
    )
    
    await Console(travel_agent_streaming.run_stream(task=task))

async def main():
    """Main function to run both demonstrations."""
    
    # Run non-streaming parallel tools demo
    # await demonstrate_parallel_tools()
    
    # Run streaming parallel tools demo
    await demonstrate_streaming_with_parallel_tools()

if __name__ == "__main__":
    asyncio.run(main())