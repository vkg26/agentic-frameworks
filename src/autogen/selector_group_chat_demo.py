import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# Create Azure OpenAI model client
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

# Function for counting down
async def countdown(start_number: int) -> str:
    """
    Count down from a given number to 0.
    
    Args:
        start_number: The number to start counting down from
        
    Returns:
        A string showing the countdown sequence
    """
    if start_number < 0:
        return "Cannot count down from a negative number!"
    
    countdown_sequence = []
    for i in range(start_number, -1, -1):
        countdown_sequence.append(str(i))
        # Add a small delay to make it feel more realistic
        await asyncio.sleep(0.1)
    
    result = " → ".join(countdown_sequence)
    return f"Countdown complete: {result}"

# Create the countdown tool
countdown_tool = FunctionTool(countdown, description="Count down from a given number to 0")

async def streaming_selector_example():
    """Demonstrate streaming SelectorGroupChat."""
    print("=== STREAMING SELECTOR GROUP CHAT COUNTDOWN EXAMPLE ===")
    print("Watch the agent selection and countdown in real-time\n")
    
    # Create agents
    user_proxy = UserProxyAgent(
        "user_proxy",
        description="Provides numbers for countdown. Type 'FINISHED' when done with all countdowns.",
    )

    assistant_agent = AssistantAgent(
        "assistant",
        model_client=az_model_client,
        tools=[countdown_tool],
        system_message=(
            "You are a countdown specialist. When given a number, use your countdown function. "
            "Be enthusiastic about counting down! After each countdown, ask if they want another one."
        ),
    )

    # Create termination condition
    termination = TextMentionTermination("FINISHED")

    # Define custom selector prompt for better agent selection
    selector_prompt = """You are an intelligent agent selector for a countdown demonstration team.

Your team consists of:
1. user_proxy: A user proxy agent that provides numbers and user input
2. assistant: An assistant agent with countdown functionality that can count from any number down to 0

Selection Guidelines:
- Choose 'user_proxy' when:
  * We need user input or a number to count down from
  * The conversation is waiting for user response
  * We need to gather requirements or preferences

- Choose 'assistant' when:
  * A number has been provided and needs countdown processing
  * We need to use the countdown function tool
  * We need to explain countdown results or ask follow-up questions

Always select the most appropriate agent based on the current conversation context and what action is needed next."""

    # Create selector team with custom prompt
    team = SelectorGroupChat(
        [user_proxy, assistant_agent],
        model_client=az_model_client, 
        termination_condition=termination,
        selector_prompt=selector_prompt
    )

    # Stream the conversation
    await Console(
        team.run_stream(
            task="Let's do some countdowns! Give me a number between 1-15 to count down from."
        )
    )
    
    return team

async def main():
    """Run SelectorGroupChat countdown examples."""
    print("SELECTOR GROUP CHAT COUNTDOWN DEMONSTRATIONS")
    print("=" * 60)
    print("This demo showcases SelectorGroupChat with countdown functionality.\n")
    
    try:
        # Run streaming example
        await streaming_selector_example()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the model client
        await az_model_client.close()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("✓ Streaming SelectorGroupChat: Real-time agent selection and countdown")
    print("✓ Custom Selector Prompt: Intelligent agent selection guidance")
    print("✓ UserProxyAgent: Provides input numbers for countdown")
    print("✓ AssistantAgent: Uses countdown function tool for counting")
    print("✓ Function Tools: countdown() function for counting down to 0")
    print("\nStreaming SelectorGroupChat with custom selector prompt enables precise agent collaboration!")

if __name__ == "__main__":
    asyncio.run(main())