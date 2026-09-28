# This tool performs web searches using the Tavily API.
# It loads the API key from environment variables and sends the search query.
# It processes and formats the returned results for easy use.
# It also handles errors such as invalid queries, API failures, and missing results.


from tavily import TavilyClient
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# get the API key from environment variables
api_key = os.getenv("TAVILY_API_KEY")

# create a Tavily client instance
client = TavilyClient(api_key=api_key)

# function to run search query using Tavily API
def tavily_search(query):
    try:
        response = client.search(
            query=query,
            max_results=5
        )

        results = []

        for i, r in enumerate(response["results"], 1):
            title = r.get("title", "Unknown")
            url = r.get("url", "")
            snippet = r.get("content", "").strip()

            results.append(f"{i}. **{title}**\n{snippet}")

        return "\n\n".join(results)

    except Exception as e:
        print(f"An error occurred while searching: {e}")
        return "Sorry, I couldn't perform the search right now."