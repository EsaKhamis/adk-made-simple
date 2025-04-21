# ADK Made Simple - Agent Examples

This project demonstrates simple agents built using the Google Agent Development Kit (ADK).

## Agents

-   **Reddit Scout**: Fetches recent discussion titles from game development subreddits using PRAW or mock data.
-   **Async Reddit Scout**: Fetches hot post titles from specified subreddits using ADK's built-in MCP Reddit tools.

## General Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd adk-made-simple
    ```

2.  **Create and activate a virtual environment (Recommended):**

    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install general dependencies:**

    ```bash
    pip install -r requirements.txt
    # This includes google-adk, praw (for reddit_scout), python-dotenv, and uvx (for async_reddit_scout).
    ```

4.  **Agent-Specific Setup:** Navigate to the specific agent's directory within `agents/` and follow the instructions in its `README.md` (or follow the steps below for the default agent).

## Reddit Scout - Setup & Running

1.  **Navigate to Agent Directory:**

    ```bash
    cd agents/reddit_scout
    ```

2.  **Set up API Keys:**

    -   Copy the example environment file **to the project root directory (`adk-made-simple/`)**:
        ```bash
        # From the project root
        cp .env.example .env
        ```
    -   Edit the root `.env` file and add your Google AI API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).
        ```dotenv
        GOOGLE_API_KEY=YOUR_API_KEY_HERE
        ```
    -   **For the PRAW-based `reddit_scout` agent**, you also need Reddit API credentials in the same `.env` file. Get these by creating a 'script' app on [Reddit Apps](https://www.reddit.com/prefs/apps).
        ```dotenv
        REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID
        REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET
        REDDIT_USER_AGENT=YOUR_APP_NAME (e.g., GameDevNewsBot/0.1 by YourUsername)
        ```
    -   _Note:_ The agents use `python-dotenv` to load these variables from the `.env` file in the project root.

3.  **Run the Agent:**

    -   Make sure your virtual environment (from the root directory) is activated.
    -   From the project root (`adk-made-simple`), run the agent using the ADK CLI:
        ```bash
        adk run agents.reddit_scout
        ```

4.  **Interact:** The agent will start, and you can interact with it in the terminal. Try prompts like:
    -   `What's the latest gamedev news?`
    -   `Give me news from unrealengine`
    -   `Check unity3d`

## Async Reddit Scout - Setup & Running

1.  **Navigate to Project Root:** Ensure you are in the main `adk-made-simple` directory.

2.  **Set up API Key & Prerequisites:**

    -   Ensure you have a `.env` file in the project root (as described in the `Reddit Scout` setup above) containing your `GOOGLE_API_KEY`.
    -   **Ensure `uvx` is installed:** This agent requires `uvx` to run the external `mcp-reddit` server. If you haven't already, run `pip install uvx` (it's included in `requirements.txt`).
    -   This agent uses MCP tools via `uvx`. The `uvx` tool handles fetching and running the `@mcp-reddit/server`. No specific Reddit keys are needed in `.env` for this agent.

3.  **Run the Agent:**

    -   Make sure your virtual environment is activated.
    -   From the project root (`adk-made-simple`), run the agent:
        ```bash
        adk run agents.async_reddit_scout
        ```

4.  **Interact:** The agent will start. Try prompts like:
    -   `What's hot in gamedev?`
    -   `Show me hot posts from unrealengine`
    -   `Fetch from unity3d`

## Project Structure Overview

```
adk-made-simple/
├── agents/
│   ├── reddit_scout/        # Reddit Scout Agent (PRAW/Mock)
│   │   ├── __init__.py
│   │   └── agent.py
│   └── async_reddit_scout/  # Async Reddit Scout Agent (MCP Tools)
│       ├── __init__.py
│       └── agent.py
├── .venv/                   # Virtual environment directory
├── .env.example             # Environment variables example
├── .gitignore               # Root gitignore file
├── requirements.txt         # Project dependencies
├── README.md                # This file (Overall Project README)
└── PLAN.md                  # Development plan notes
```
