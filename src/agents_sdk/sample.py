from agents import GuardrailFunctionOutput, Agent, Runner, InputGuardrail, FunctionTool, RunContextWrapper, \
    function_tool, WebSearchTool, ItemHelpers
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
import json
from typing_extensions import TypedDict, Any
from agents import set_default_openai_key

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

# # Set the OpenAI API Key
# os.environ["OPENAI_API_KEY"] =


async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())