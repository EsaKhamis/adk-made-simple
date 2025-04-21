import asyncio
import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

async def get_tools_async():
    """Connects to the mcp-reddit server via uvx and returns the tools and exit stack."""
    print("--- Attempting to start and connect to mcp-reddit MCP server via uvx ---")
    try:
        # Check if uvx is available (basic check)
        # A more robust check might involve checking the actual command's success
        await asyncio.create_subprocess_shell('uvx --version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='uvx',
                args=['--from', 'git+https://github.com/adhikasp/mcp-reddit.git', 'mcp-reddit'],
                # Optional: Add environment variables if needed by the MCP server,
                # e.g., credentials if mcp-reddit required them.
                # env=os.environ.copy()
            )
        )
        print(f"--- Successfully connected to mcp-reddit server. Discovered {len(tools)} tool(s). ---")
        # Print discovered tool names for debugging/instruction refinement
        for tool in tools:
            print(f"  - Discovered tool: {tool.name}") # Tool name is likely 'fetch_reddit_hot_threads' or similar
        return tools, exit_stack
    except FileNotFoundError:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! ERROR: 'uvx' command not found. Please install uvx: pip install uvx !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Return empty tools and a no-op exit stack to prevent agent failure
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
        return [], DummyExitStack()
    except Exception as e:
        print(f"--- ERROR connecting to or starting mcp-reddit server: {e} ---")
        # Return empty tools and a no-op exit stack
        class DummyExitStack:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
        return [], DummyExitStack()


async def create_agent():
    """Creates the agent instance after fetching tools from the MCP server."""
    tools, exit_stack = await get_tools_async()

    # IMPORTANT: Adjust the instruction based on the *actual* tool name discovered
    # by mcp-reddit (likely 'fetch_reddit_hot_threads'). Check the print statement above when running.
    # If no tools are discovered due to an error, the agent won't have the tool.
    discovered_tool_name = "fetch_reddit_hot_threads" # <-- ASSUMPTION, VERIFY FROM OUTPUT!
    if not tools:
         print("--- WARNING: No tools discovered from MCP server. Agent will lack Reddit functionality. ---")

    agent_instance = Agent(
        name="async_reddit_scout_agent",
        description="A Reddit scout agent that searches for hot posts in a given subreddit using an external MCP Reddit tool.",
        model="gemini-1.5-flash-latest", # Ensure API key is in .env
        instruction=(
            "You are the Async Game Dev News Scout. Your task is to fetch hot post titles from game development subreddits using the connected Reddit MCP tool."
            "1. **Identify Subreddit:** Determine which subreddit the user wants news from. Default to 'gamedev' if none is specified. Use the specific subreddit mentioned (e.g., 'unity3d', 'unrealengine')."
            f"2. **Call Discovered Tool:** You **MUST** look for and call the tool named '{discovered_tool_name}' with the identified subreddit name and optionally a limit." # Adjust name if needed!
            "3. **Present Results:** The tool will return a formatted string containing the hot post information or an error message."
            "   - Present this string directly to the user."
            "   - Clearly state which subreddit the information is from."
            "   - If the tool returns an error message, relay that message accurately."
            "4. **Handle Missing Tool:** If you cannot find the required Reddit tool, inform the user that you cannot fetch Reddit news due to a configuration issue."
            "5. **Do Not Hallucinate:** Only provide information returned by the tool."
        ),
        tools=tools, # Pass the discovered tools
        # Note: We don't explicitly pass exit_stack here.
        # ADK's runner mechanism when loading an async factory or
        # awaitable like 'agent = create_agent()' should handle the lifecycle.
        # If issues arise, we might need to manage the exit_stack more explicitly.
    )
    # Store exit_stack somewhere accessible if needed for manual cleanup later,
    # though ideally ADK handles it. For adk run, this might be tricky.
    # setattr(agent_instance, '_mcp_exit_stack', exit_stack) # Example, may not be necessary
    # ADK needs the exit_stack to manage the MCP server process lifecycle.
    # Return both the agent instance and the exit_stack.
    return agent_instance, exit_stack

# ADK runner expects an 'agent' or 'root_agent' variable.
# Assign the awaitable coroutine object, following the documentation pattern.
# If this causes 'cannot reuse already awaited coroutine' with 'adk run',
# it indicates a lifecycle mismatch with the runner for this pattern.
root_agent = create_agent()

# Keep the example __main__ block commented out, as 'adk run' is the primary execution method.
# # Example of how to potentially use it later (requires Runner, etc.)
# # if __name__ == '__main__':
# # ... (rest of the commented block remains unchanged) 