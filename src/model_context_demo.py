from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_core.model_context import (
    BufferedChatCompletionContext,
    TokenLimitedChatCompletionContext,
    UnboundedChatCompletionContext
)
import asyncio, os
from dotenv import load_dotenv

load_dotenv()

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

# Simple tools for demonstration
async def get_current_time() -> str:
    """Get the current time."""
    import datetime
    return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

async def add_numbers(a: int, b: int) -> str:
    """Add two numbers together."""
    return f"The sum of {a} and {b} is {a + b}"

async def get_random_fact() -> str:
    """Get a random interesting fact."""
    facts = [
        "Octopuses have three hearts and blue blood.",
        "Honey never spoils and can be edible after thousands of years.",
        "A group of flamingos is called a 'flamboyance'.",
        "Bananas are berries, but strawberries aren't.",
        "There are more possible chess games than atoms in the observable universe."
    ]
    import random
    return f"Random fact: {random.choice(facts)}"

# Create strict tools
time_tool = FunctionTool(get_current_time, description="Get current time", strict=True)
math_tool = FunctionTool(add_numbers, description="Add two numbers", strict=True)
fact_tool = FunctionTool(get_random_fact, description="Get a random fact", strict=True)

async def demonstrate_unbounded_context():
    """Demonstrate UnboundedChatCompletionContext (default behavior)."""
    print("=== UNBOUNDED CONTEXT DEMO ===")
    print("This agent remembers ALL conversation history\n")
    
    # Default context - remembers everything
    unbounded_agent = AssistantAgent(
        name="unbounded_assistant",
        model_client=az_model_client,
        tools=[time_tool, math_tool, fact_tool],
        system_message="You are a helpful assistant. Always remember our conversation history.",
        model_context=UnboundedChatCompletionContext(),  # This is the default
        reflect_on_tool_use=True,
    )
    
    # Have a multi-turn conversation
    tasks = [
        "What's the current time?",
        "Add 25 and 17 together",
        "Tell me a random fact",
        "What was the first thing I asked you?",  # Test memory
        "What numbers did I ask you to add?",    # Test memory
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Turn {i}: {task} ---")
        result = await unbounded_agent.run(task=task)
        print(f"Response: {result.messages[-1].content}")
    
    # Access messages through the model context instead of _memory
    context_messages = await unbounded_agent.model_context.get_messages()
    print(f"\nTotal messages in context: {len(context_messages)}")

async def demonstrate_buffered_context():
    """Demonstrate BufferedChatCompletionContext (limited message history)."""
    print("\n\n=== BUFFERED CONTEXT DEMO ===")
    print("This agent only remembers the last 3 messages\n")
    
    # Limited context - only remembers last N messages
    buffered_agent = AssistantAgent(
        name="buffered_assistant",
        model_client=az_model_client,
        tools=[time_tool, math_tool, fact_tool],
        system_message="You are a helpful assistant.",
        model_context=BufferedChatCompletionContext(buffer_size=3),  # Only last 3 messages
        reflect_on_tool_use=True,
    )
    
    # Have the same conversation
    tasks = [
        "What's the current time?",
        "Add 25 and 17 together", 
        "Tell me a random fact",
        "What was the first thing I asked you?",  # Should not remember
        "What numbers did I ask you to add?",    # Might not remember
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Turn {i}: {task} ---")
        result = await buffered_agent.run(task=task)
        print(f"Response: {result.messages[-1].content}")
        
        # Access messages through the model context
        context_messages = await buffered_agent.model_context.get_messages()
        print(f"Messages in context: {len(context_messages)}")

async def demonstrate_token_limited_context():
    """Demonstrate TokenLimitedChatCompletionContext (limited by token count)."""
    print("\n\n=== TOKEN LIMITED CONTEXT DEMO ===")
    print("This agent is limited by token count (500 tokens)\n")
    
    # Token-limited context
    token_limited_agent = AssistantAgent(
        name="token_limited_assistant", 
        model_client=az_model_client,
        tools=[time_tool, math_tool, fact_tool],
        system_message="You are a helpful assistant that provides detailed explanations.",
        model_context=TokenLimitedChatCompletionContext(max_tokens=500),  # 500 token limit
        reflect_on_tool_use=True,
    )
    
    # Ask for increasingly detailed responses to fill up token limit
    tasks = [
        "Explain what machine learning is in detail",
        "Now explain deep learning and neural networks", 
        "What is artificial intelligence?",
        "What was the first thing I asked about?",  # Test if early messages are forgotten
    ]
    
    for i, task in enumerate(tasks, 1):
        print(f"\n--- Turn {i}: {task} ---")
        result = await token_limited_agent.run(task=task)
        print(f"Response: {result.messages[-1].content[:200]}...")  # Truncate for display
        
        # Access messages through the model context
        context_messages = await token_limited_agent.model_context.get_messages()
        print(f"Messages in context: {len(context_messages)}")

async def main():
    """Run all model context demonstrations."""
    print("MODEL CONTEXT DEMONSTRATION")
    print("=" * 50)
    print("This demo shows how different model context strategies affect agent memory and behavior.\n")
    
    # Run all demonstrations
    # await demonstrate_unbounded_context()
    await demonstrate_buffered_context() 
    # await demonstrate_token_limited_context()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("1. UnboundedChatCompletionContext: Remembers entire conversation history")
    print("2. BufferedChatCompletionContext: Limits memory to last N messages")  
    print("3. TokenLimitedChatCompletionContext: Limits memory by token count")
    print("4. Choose the right context strategy based on your use case!")

if __name__ == "__main__":
    asyncio.run(main())