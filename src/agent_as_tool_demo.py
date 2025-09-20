import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

# Create Azure OpenAI model client - IMPORTANT: Disable parallel tool calls for AgentTool
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    parallel_tool_calls=False  # CRITICAL: Must disable for AgentTool to work properly
)

async def agent_as_tool_demo():
    """
    Demonstrate the Agent as a Tool pattern where specialized agents 
    are used as tools by a coordinator agent.
    """
    print("=== AGENT AS A TOOL DEMO ===")
    print("Showing how to use specialized agents as tools in AutoGen\n")
    
    # Create specialized expert agents
    
    # Math Expert Agent
    math_expert = AssistantAgent(
        name="math_expert",
        model_client=az_model_client,
        system_message="""You are a mathematics expert.
        Solve mathematical problems step by step.
        Show your work clearly and provide accurate calculations.
        Focus only on mathematical concepts and computations.""",
        description="A specialized agent for solving mathematical problems and calculations.",
        model_client_stream=True
    )
    
    # Chemistry Expert Agent  
    chemistry_expert = AssistantAgent(
        name="chemistry_expert", 
        model_client=az_model_client,
        system_message="""You are a chemistry expert.
        Explain chemical concepts, reactions, and molecular structures.
        Provide accurate chemical formulas and balanced equations.
        Focus only on chemistry-related topics.""",
        description="A specialized agent for chemistry questions and chemical analysis.",
        model_client_stream=True
    )
    
    # Writing Expert Agent
    writing_expert = AssistantAgent(
        name="writing_expert",
        model_client=az_model_client, 
        system_message="""You are a writing and language expert.
        Help with grammar, style, composition, and editing.
        Provide clear explanations and writing improvements.
        Focus only on language and writing topics.""",
        description="A specialized agent for writing, editing, and language assistance.",
        model_client_stream=True
    )
    
    # Convert agents to tools using AgentTool
    math_tool = AgentTool(
        agent=math_expert,
        description="Use this tool for mathematical calculations and problem solving",
        return_value_as_last_message=True  # Return the agent's final response
    )
    
    chemistry_tool = AgentTool(
        agent=chemistry_expert,
        description="Use this tool for chemistry questions and chemical analysis", 
        return_value_as_last_message=True
    )
    
    writing_tool = AgentTool(
        agent=writing_expert,
        description="Use this tool for writing help and language assistance",
        return_value_as_last_message=True
    )
    
    # Create coordinator agent that uses specialist agents as tools
    coordinator = AssistantAgent(
        name="coordinator",
        model_client=az_model_client,
        system_message="""You are a helpful assistant coordinator.
        You have access to expert agents as tools for specialized tasks:
        - math_expert: For mathematical problems and calculations
        - chemistry_expert: For chemistry questions and chemical analysis  
        - writing_expert: For writing and language assistance
        
        When you receive a question:
        1. Determine which expert would be most appropriate
        2. Use the corresponding tool to get expert assistance
        3. Relay the expert's response to the user
        
        Use the expert tools when the question requires specialized knowledge.""",
        tools=[math_tool, chemistry_tool, writing_tool],
        model_client_stream=True,
        max_tool_iterations=3  # Allow multiple tool calls if needed
    )
    
    # Test different types of questions
    test_questions = [
        "What is the integral of x^2 from 0 to 3?",
        "What is the molecular formula for caffeine and explain its structure?", 
        "Can you help me improve this sentence: 'The dog was walked by me'?",
        "If I have a triangle with sides 3, 4, and 5, what is its area?"
    ]
    
    print("Testing different questions that require specialized expertise:\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"--- Question {i} ---")
        print(f"User: {question}\n")
        
        # Run the coordinator with streaming output
        result = await Console(coordinator.run_stream(task=question))
        
        print(f"\n✅ Response completed for question {i}")
        print("-" * 60)
        
        # Small delay between questions for readability
        await asyncio.sleep(1)
    
    return coordinator

async def main():
    """Run the Agent as a Tool demonstration."""
    print("AGENT AS A TOOL PATTERN DEMONSTRATION")
    print("=" * 60)
    print("Showcasing how to use specialized agents as tools\n")
    
    try:
        await agent_as_tool_demo()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the model client
        await az_model_client.close()
    
    print("\n" + "=" * 60)
    print("AGENT AS A TOOL PATTERN BENEFITS:")
    print("✓ Modular Design: Specialized agents for specific domains")
    print("✓ Reusable Experts: Same agents can be used across workflows") 
    print("✓ Dynamic Routing: Coordinator intelligently selects appropriate expert")
    print("✓ Tool Integration: Agents become callable tools with schemas")
    print("✓ Scalable Architecture: Easy to add new expert agents")
    print("✓ Maintainable Code: Clear separation of concerns")
    print("\nAgent as a Tool enables powerful multi-agent orchestration!")

if __name__ == "__main__":
    asyncio.run(main())