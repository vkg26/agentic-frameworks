from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import asyncio, os
from dotenv import load_dotenv

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
    return f"The weather in {city} is 73 degrees and Sunny."


agent = AssistantAgent(
    name="weather_agent",
    model_client=az_model_client,
    tools=[get_weather],
    system_message="You are a helpful assistant.",
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


# Run the agent and stream the messages to the console.
async def main() -> None:
    await Console(agent.run_stream(task="What is the weather in New York?"))


asyncio.run(main())
