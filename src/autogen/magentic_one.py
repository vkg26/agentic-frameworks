import asyncio, os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne
from autogen_agentchat.ui import Console

load_dotenv()
model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

async def example_usage():
    m1 = MagenticOne(client=model_client)
    task = "Write a Python script to print a fibonacci sequence till 10. Execute it and print the output."
    result = await Console(m1.run_stream(task=task))
    print(result)


if __name__ == "__main__":
    asyncio.run(example_usage())
