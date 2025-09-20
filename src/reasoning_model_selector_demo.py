import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from typing import List
import random
import time

load_dotenv()

# Create Azure OpenAI model client - Using o3-mini for reasoning model capabilities
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL_REASONING"),  # Should be o3-mini or similar reasoning model
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

# Mock tools for demonstration purposes
async def search_tool(query: str) -> str:
    """
    A mock search tool that simulates finding information.
    
    Args:
        query: The search query
        
    Returns:
        Mock search results based on the query
    """
    await asyncio.sleep(0.5)  # Simulate search delay
    
    if "weather" in query.lower():
        locations = ["New York", "London", "Tokyo", "Sydney", "Paris"]
        location = random.choice(locations)
        temp = random.randint(15, 85)
        return f"Weather in {location}: {temp}°F, partly cloudy with light winds."
    
    elif "news" in query.lower():
        topics = ["technology", "sports", "science", "business", "entertainment"]
        topic = random.choice(topics)
        return f"Latest {topic} news: Major breakthrough announced in {topic} sector with significant implications."
    
    elif "stock" in query.lower() or "market" in query.lower():
        companies = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
        company = random.choice(companies)
        price = random.randint(100, 500)
        change = random.uniform(-5, 5)
        return f"{company} stock price: ${price:.2f}, change: {change:+.2f}%"
    
    else:
        return f"Search results for '{query}': Found relevant information about {query} with multiple data points and sources."

async def calculate_tool(expression: str) -> str:
    """
    A calculator tool that performs mathematical operations.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        The result of the calculation
    """
    try:
        # Simple evaluation for demo purposes
        # In production, use a proper math parser for security
        allowed_chars = set('0123456789+-*/.() ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"Calculation result: {expression} = {result}"
        else:
            return "Error: Invalid characters in expression. Only numbers and basic operators allowed."
    except Exception as e:
        return f"Error: Could not calculate '{expression}'. {str(e)}"

async def data_analysis_tool(data_points: str) -> str:
    """
    A tool that performs basic data analysis.
    
    Args:
        data_points: Comma-separated numbers to analyze
        
    Returns:
        Statistical analysis of the data
    """
    try:
        numbers = [float(x.strip()) for x in data_points.split(',')]
        if not numbers:
            return "Error: No valid numbers provided"
        
        mean = sum(numbers) / len(numbers)
        minimum = min(numbers)
        maximum = max(numbers)
        
        return f"Data analysis: Count={len(numbers)}, Mean={mean:.2f}, Min={minimum}, Max={maximum}"
    except Exception as e:
        return f"Error: Could not analyze data '{data_points}'. {str(e)}"

# Create function tools
search_function_tool = FunctionTool(search_tool, description="Search for information on various topics")
calculate_function_tool = FunctionTool(calculate_tool, description="Perform mathematical calculations")
analysis_function_tool = FunctionTool(data_analysis_tool, description="Analyze numerical data")

async def reasoning_model_selector_demo():
    """
    Demonstrate SelectorGroupChat with reasoning models using simplified prompts.
    Key principle: Reasoning models work best with minimal, clear instructions.
    """
    print("=== REASONING MODEL SELECTOR GROUP CHAT DEMO ===")
    print("Using simplified prompts optimized for reasoning models like o3-mini\n")
    
    # Create agents with minimal system messages (key for reasoning models)
    search_agent = AssistantAgent(
        "SearchAgent",
        description="An agent that searches for information.",
        tools=[search_function_tool],
        model_client=az_model_client,
        system_message="Use search tool to find information."  # Minimal instruction
    )

    calculator_agent = AssistantAgent(
        "CalculatorAgent", 
        description="An agent that performs calculations.",
        tools=[calculate_function_tool],
        model_client=az_model_client,
        system_message="Use calculator tool for math."  # Minimal instruction
    )

    analyst_agent = AssistantAgent(
        "AnalystAgent",
        description="An agent that analyzes data.",
        tools=[analysis_function_tool],
        model_client=az_model_client,
        system_message="Use analysis tool for data."  # Minimal instruction
    )

    user_proxy = UserProxyAgent(
        "UserProxy",
        description="A user to provide feedback and approval."
    )

    # Simple selector prompt optimized for reasoning models
    selector_prompt = """Select an agent to perform task.

{roles}

Current conversation:
{history}

Select one agent from {participants} to handle the next task.
When task is complete, get user approval."""

    # Termination conditions
    text_termination = TextMentionTermination("FINISHED")
    max_messages_termination = MaxMessageTermination(max_messages=20)
    termination = text_termination | max_messages_termination

    # Create team with reasoning model optimizations
    team = SelectorGroupChat(
        [search_agent, calculator_agent, analyst_agent, user_proxy],
        model_client=az_model_client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
        allow_repeated_speaker=True  # Allow agents to continue working
    )

    # Stream the conversation to see reasoning model in action
    task = """I need to:
1. Search for current weather information
2. Calculate the average of these numbers: 25, 30, 35, 40
3. Analyze the data trends

Please complete these tasks and get my approval when done."""

    await Console(team.run_stream(task=task))
    
    return team

async def main():
    """Run reasoning model SelectorGroupChat demonstrations."""
    print("REASONING MODEL SELECTOR GROUP CHAT DEMONSTRATIONS")
    print("=" * 65)
    print("Key Principle: Reasoning models (o3-mini) work best with SIMPLE prompts")
    print("Complex instructions can actually hurt performance!\n")
    
    try:
        # Run reasoning model demo
        await reasoning_model_selector_demo()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the model client
        await az_model_client.close()
    
    print("\n" + "=" * 65)
    print("REASONING MODEL BEST PRACTICES:")
    print("✓ Use MINIMAL system messages (1-5 words ideal)")
    print("✓ Keep selector prompts SIMPLE and direct")
    print("✓ Avoid detailed step-by-step instructions")
    print("✓ Let the reasoning model figure out the approach")
    print("✓ Trust the model's internal reasoning process")
    print("✓ No planning agent needed - selector handles planning")
    print("\nReasoning models excel with minimal guidance and maximum autonomy!")

if __name__ == "__main__":
    asyncio.run(main())