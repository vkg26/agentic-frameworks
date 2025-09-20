import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination, TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv()

# Create Azure OpenAI model client
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
)

async def basic_round_robin_example():
    """Demonstrate basic Round Robin Group Chat with reflection pattern."""
    print("=== BASIC ROUND ROBIN GROUP CHAT EXAMPLE ===")
    print("Demonstrates the reflection pattern with primary agent, critic agent, and user proxy\n")
    
    # Create the primary agent
    primary_agent = AssistantAgent(
        "primary",
        model_client=az_model_client,
        system_message="You are a helpful AI assistant that writes creative content.",
    )

    # Create the critic agent
    critic_agent = AssistantAgent(
        "critic",
        model_client=az_model_client,
        system_message="Provide constructive feedback on creative writing.",
    )

    # Create the user proxy agent
    user_proxy = UserProxyAgent(
        "user_proxy",
        description="A user proxy agent that represents human feedback. Say 'HAPPY' when satisfied with the content.",
    )

    # Define a termination condition that stops the task when user proxy says "HAPPY"
    text_termination = TextMentionTermination("HAPPY")

    # Create a team with three agents: primary, critic, and user proxy
    team = RoundRobinGroupChat([primary_agent, critic_agent, user_proxy], termination_condition=text_termination)

    # Run the team with a task
    result = await team.run(task="Write a short poem about the fall season.")
    
    print("=== FINAL RESULT ===")
    print(f"Stop reason: {result.stop_reason}")
    print(f"Total messages: {len(result.messages)}")
    print("\nFinal message:")
    print(result.messages[-1].content)
    
    return team

async def streaming_round_robin_example():
    """Demonstrate streaming Round Robin Group Chat."""
    print("\n\n=== STREAMING ROUND ROBIN GROUP CHAT EXAMPLE ===")
    print("Watch the conversation unfold in real-time with three agents\n")
    
    # Create agents
    writer_agent = AssistantAgent(
        "writer",
        model_client=az_model_client,
        system_message="You are a creative writer who specializes in short stories.",
    )

    editor_agent = AssistantAgent(
        "editor",
        model_client=az_model_client,
        system_message="You are an editor who provides feedback on story structure, pacing, and engagement.",
    )

    # Create user proxy agent
    user_proxy = UserProxyAgent(
        "user_proxy",
        description="A user proxy agent that represents human feedback. Say 'HAPPY' when the story meets your expectations.",
    )

    # Create termination condition looking for "HAPPY"
    termination = TextMentionTermination("HAPPY")

    # Create team with three agents
    team = RoundRobinGroupChat([writer_agent, editor_agent, user_proxy], termination_condition=termination)

    # Stream the conversation
    await Console(team.run_stream(task="Write a very short mystery story with a twist ending."))
    
    return team

async def main():
    """Run Round Robin Group Chat examples."""
    print("ROUND ROBIN GROUP CHAT DEMONSTRATIONS")
    print("=" * 60)
    print("This demo showcases basic AutoGen Round Robin Group Chat functionality.\n")
    
    try:
        # Run examples
        # await basic_round_robin_example()
        await streaming_round_robin_example()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the model client
        await az_model_client.close()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("✓ Basic Round Robin: Three agents collaborating with reflection pattern")
    print("✓ Streaming: Real-time conversation viewing with user proxy agent")  
    print("✓ User Proxy: Represents human feedback and says 'HAPPY' for termination")
    print("\nRound Robin Group Chat enables powerful multi-agent collaboration!")

if __name__ == "__main__":
    asyncio.run(main())