# Async Reddit Scout Agent

This agent uses the ADK's built-in MCP Reddit tools (`mcp_reddit_fetch_reddit_hot_threads`) to fetch hot posts from specified subreddits.

## Setup

-   Ensure you have a `.env` file in the project root (`adk-made-simple/`) containing your `GOOGLE_API_KEY`.
-   **Install `uvx`:** This agent requires `uvx` to run the external `mcp-reddit` server. Make sure it's installed via `pip install uvx` (included in the root `requirements.txt`).
-   No specific Reddit API keys are needed in the `.env` file for this agent when running locally, as the `mcp-reddit` server launched by `uvx` handles its own authentication if required (though it might be anonymous access by default).

## Running

1.  Activate your virtual environment from the project root.
2.  Run the agent using the ADK CLI from the project root:
    ```bash
    adk run agents.async_reddit_scout
    ``` 