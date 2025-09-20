from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
import asyncio, os
from dotenv import load_dotenv
from pydantic import BaseModel

class WeatherResponse(BaseModel):
    city: str
    temperature: str
    condition: str
    summary: str

load_dotenv()
print("API Key:", os.getenv("API_KEY"))  # For debugging, remove this in production

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

async def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"Weather data for {city}: Temperature is 73°F, condition is sunny with clear skies, humidity 45%, wind 5mph from the west."

# Create a strict function tool
get_weather_tool = FunctionTool(get_weather, description="Get the weather for a given city", strict=True)


agent = AssistantAgent(
    name="weather_agent",
    model_client=az_model_client,
    tools=[get_weather_tool],
    system_message="You are a helpful assistant that provides weather information in structured format.",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
    output_content_type=WeatherResponse,  # Generate structured output using Pydantic model
)


# Run the agent with both streaming and non-streaming options.
async def main() -> None:
    # Non-streaming version (currently active)
    # response = await agent.run(task="What is the weather in New York?")
    # print("Agent Response:")
    # print(response)
    
    # Streaming version (commented out)
    await Console(agent.run_stream(task="What is the weather in New York?"))

    # OR support streaming through async function and iteration
    # Use an async function and asyncio.run() in a script.
    # async for message in agent.run_stream(task="Name two cities in South America"):  # type: ignore
    #     print(message)


asyncio.run(main())
