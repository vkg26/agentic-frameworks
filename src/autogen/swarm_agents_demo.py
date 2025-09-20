import asyncio
from typing import Any, Dict, List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.teams import Swarm
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Create Azure OpenAI model client with parallel tool calls disabled for better handoff behavior
az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("DEPLOYMENT_NAME"),
    model=os.getenv("MODEL"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("API_KEY"),
    parallel_tool_calls=False  # Important: Disable parallel tool calls for better handoff control
)

# Mock tools for demonstration
async def process_order(order_id: str, action: str) -> str:
    """Process an order with the specified action."""
    actions = {
        "cancel": f"Order {order_id} has been successfully cancelled. Refund will be processed within 3-5 business days.",
        "modify": f"Order {order_id} has been modified. Updated confirmation will be sent to your email.",
        "track": f"Order {order_id} is currently in transit. Expected delivery: 2-3 business days.",
        "expedite": f"Order {order_id} has been expedited. New delivery estimate: 1-2 business days (additional charges may apply)."
    }
    await asyncio.sleep(0.5)  # Simulate processing time
    return actions.get(action, f"Action '{action}' completed for order {order_id}")

async def check_inventory(product_name: str) -> str:
    """Check inventory status for a product."""
    products = {
        "laptop": "In stock - 15 units available",
        "headphones": "Low stock - 3 units remaining", 
        "mouse": "In stock - 50+ units available",
        "keyboard": "Out of stock - Expected restock in 1 week",
        "monitor": "In stock - 8 units available"
    }
    await asyncio.sleep(0.3)
    return products.get(product_name.lower(), f"Product '{product_name}' not found in inventory")

async def calculate_shipping(weight: float, destination: str) -> str:
    """Calculate shipping cost and time."""
    base_cost = 5.99
    weight_cost = weight * 1.50
    
    destinations = {
        "domestic": {"multiplier": 1.0, "days": "2-3"},
        "international": {"multiplier": 2.5, "days": "7-10"},
        "express": {"multiplier": 1.8, "days": "1-2"}
    }
    
    dest_info = destinations.get(destination.lower(), destinations["domestic"])
    total_cost = (base_cost + weight_cost) * dest_info["multiplier"]
    
    await asyncio.sleep(0.4)
    return f"Shipping to {destination}: ${total_cost:.2f}, Estimated delivery: {dest_info['days']} business days"

async def generate_report(data_type: str) -> str:
    """Generate various types of reports."""
    reports = {
        "sales": "Sales Report Generated: Total sales this month: $125,430. Top product: Laptops (45 units sold).",
        "inventory": "Inventory Report Generated: 234 total items in stock. 12 items low stock. 3 items out of stock.",
        "customer": "Customer Report Generated: 89 new customers this month. Customer satisfaction: 94.2%.",
        "financial": "Financial Report Generated: Revenue up 15% from last month. Profit margin: 23.5%."
    }
    await asyncio.sleep(1.0)  # Reports take longer to generate
    return reports.get(data_type.lower(), f"Custom {data_type} report generated successfully")

# Create function tools
order_tool = FunctionTool(process_order, description="Process customer orders (cancel, modify, track, expedite)")
inventory_tool = FunctionTool(check_inventory, description="Check product inventory status")
shipping_tool = FunctionTool(calculate_shipping, description="Calculate shipping costs and delivery times")
report_tool = FunctionTool(generate_report, description="Generate business reports (sales, inventory, customer, financial)")

async def customer_service_swarm_demo():
    """
    Demonstrate Swarm with a customer service team that can hand off between agents.
    Shows human-in-the-loop handoffs and specialized agent interactions.
    """
    print("=== CUSTOMER SERVICE SWARM DEMO ===")
    print("Multi-agent customer service with intelligent handoffs\n")
    
    # Customer Service Representative - Main entry point
    customer_service_rep = AssistantAgent(
        "customer_service_rep",
        model_client=az_model_client,
        handoffs=["order_specialist", "inventory_specialist", "user"],
        system_message="""You are a customer service representative.
        Help customers with general inquiries and direct them to specialists when needed.
        
        Handoff to:
        - order_specialist: For order-related issues (cancel, modify, track, expedite)
        - inventory_specialist: For product availability questions
        - user: When you need more information from the customer
        
        Always greet customers warmly and ask how you can help.
        Use TERMINATE when the customer's issue is fully resolved."""
    )
    
    # Order Specialist - Handles order processing
    order_specialist = AssistantAgent(
        "order_specialist", 
        model_client=az_model_client,
        handoffs=["customer_service_rep", "user"],
        tools=[order_tool],
        system_message="""You are an order processing specialist.
        Handle all order-related requests using the process_order tool.
        
        Available actions: cancel, modify, track, expedite
        Always ask for order ID if not provided.
        
        Handoff to:
        - customer_service_rep: When order processing is complete
        - user: When you need order details from customer
        
        Be professional and confirm all actions with customers."""
    )
    
    # Inventory Specialist - Handles product inquiries
    inventory_specialist = AssistantAgent(
        "inventory_specialist",
        model_client=az_model_client, 
        handoffs=["customer_service_rep", "shipping_specialist", "user"],
        tools=[inventory_tool],
        system_message="""You are an inventory specialist.
        Check product availability using the check_inventory tool.
        
        Handoff to:
        - customer_service_rep: For general follow-up
        - shipping_specialist: If customer wants shipping info
        - user: When you need product details from customer
        
        Provide accurate stock information and suggest alternatives for out-of-stock items."""
    )
    
    # Shipping Specialist - Handles shipping calculations
    shipping_specialist = AssistantAgent(
        "shipping_specialist",
        model_client=az_model_client,
        handoffs=["customer_service_rep", "user"],
        tools=[shipping_tool],
        system_message="""You are a shipping specialist.
        Calculate shipping costs and delivery times using the calculate_shipping tool.
        
        Ask for package weight and destination type (domestic/international/express).
        
        Handoff to:
        - customer_service_rep: When shipping calculation is complete
        - user: When you need shipping details from customer
        
        Provide clear shipping options and costs."""
    )
    
    # Create termination conditions
    # Stop when handing off to user OR when TERMINATE is mentioned
    termination = HandoffTermination(target="user") | TextMentionTermination("TERMINATE")
    
    # Create Swarm team
    customer_service_team = Swarm(
        participants=[customer_service_rep, order_specialist, inventory_specialist, shipping_specialist],
        termination_condition=termination
    )
    
    # Example customer inquiry
    task = "Hi, I want to cancel my order and also check if you have any laptops in stock."
    
    print("Starting customer service interaction...")
    print(f"Customer: {task}\n")
    
    # Run the team with streaming
    task_result = await Console(customer_service_team.run_stream(task=task))
    last_message = task_result.messages[-1]
    
    # Handle user handoffs (human-in-the-loop)
    while isinstance(last_message, HandoffMessage) and last_message.target == "user":
        print(f"\n🤖 Agent {last_message.source} is requesting information from you...")
        user_input = input("Your response: ")
        
        # Continue the conversation with user input
        task_result = await Console(
            customer_service_team.run_stream(
                task=HandoffMessage(source="user", target=last_message.source, content=user_input)
            )
        )
        last_message = task_result.messages[-1]
    
    print(f"\n✅ Customer service interaction completed!")
    print(f"Final status: {task_result.stop_reason}")
    
    return customer_service_team

async def main():
    """Run Swarm demonstration."""
    print("SWARM AGENT DEMONSTRATION")
    print("=" * 50)
    print("Showcasing AutoGen Swarm with intelligent handoff patterns\n")
    
    try:
        # Run customer service demo with human-in-the-loop
        await customer_service_swarm_demo()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the model client
        await az_model_client.close()
    
    print("\n" + "=" * 50)
    print("SWARM PATTERN BENEFITS:")
    print("✓ Decentralized Decision Making: Agents make local handoff decisions")
    print("✓ Specialized Expertise: Each agent focuses on specific capabilities") 
    print("✓ Dynamic Workflow: Flexible handoff patterns based on context")
    print("✓ Human-in-the-Loop: Seamless user interaction when needed")
    print("✓ Shared Context: All agents have access to conversation history")
    print("✓ Tool Integration: Agents use specialized tools for their domain")
    print("\nSwarm enables natural, flexible multi-agent collaboration!")

if __name__ == "__main__":
    asyncio.run(main())