import os

import requests
from dotenv import load_dotenv


# Load variables from the .env file into the environment.
load_dotenv()


# Get the AviationStack API key from the environment.
API_KEY = os.getenv("AVIATION_STACK_API_KEY")


# Get the AviationStack base URL from the environment.
BASE_URL = os.getenv("AVIATION_STACK_BASE_URL")


def search_flights(
    origin: str | None = None,
    destination: str | None = None,
    limit: int = 10,
) -> dict:
    """
    Search for live flight information using the AviationStack API.

    This function is designed to be called by an AI agent. The agent
    provides structured flight search parameters, while this function
    handles the API request, authentication, error handling, and
    response extraction.

    Args:
        origin: The departure airport's IATA code, such as "NBO".
        destination: The arrival airport's IATA code, such as "NRT".
        limit: Maximum number of flight results to request.

    Returns:
        A dictionary containing either:
        - success=True and the returned flight data, or
        - success=False and an error message.
    """

    # Make sure the API credentials and endpoint have been configured.
    if not API_KEY:
        return {
            "success": False,
            "error": "AVIATION_API_KEY is not configured.",
        }

    if not BASE_URL:
        return {
            "success": False,
            "error": "AVIATION_STACK_BASE_URL is not configured.",
        }

    # Build the query parameters that AviationStack expects.
    # The access_key authenticates the request, while limit controls
    # how many flight records are returned.
    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    # Only add the departure filter when the agent provides an origin.
    # AviationStack expects the airport to be supplied as an IATA code.
    if origin:
        params["dep_iata"] = origin.upper()

    # Only add the arrival filter when the agent provides a destination.
    if destination:
        params["arr_iata"] = destination.upper()

    try:
        # Send the GET request to the AviationStack API.
        #
        # params= automatically converts the dictionary into URL
        # query parameters.
        #
        # timeout prevents the application from waiting indefinitely
        # if the API does not respond.
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30,
        )

        # Raise an exception for HTTP errors such as 401, 403,
        # 404, or 500 responses.
        response.raise_for_status()

        # Convert the JSON response from AviationStack into
        # normal Python dictionaries and lists.
        data = response.json()

    except requests.exceptions.RequestException as e:
        # Handles network-related problems and HTTP errors.
        # Returning a structured error allows the agent to understand
        # that the tool failed instead of crashing the application.
        return {
            "success": False,
            "error": f"AviationStack request failed: {str(e)}",
        }

    except ValueError:
        # Handles cases where the API response cannot be parsed
        # as valid JSON.
        return {
            "success": False,
            "error": "AviationStack returned invalid JSON.",
        }

    # AviationStack can return an API-level error inside a valid
    # HTTP response. Therefore, we need to check the response body
    # separately from HTTP errors.
    if "error" in data:
        error = data["error"]

        return {
            "success": False,
            "error": error.get(
                "message",
                "AviationStack returned an unknown error.",
            ),
        }

    # AviationStack places the actual flight records inside
    # the "data" field.
    flights = data.get("data", [])

    # Return structured data rather than formatted text.
    #
    # This is important for an agentic system because the agent
    # can decide how the results should be presented to the user.
    return {
        "success": True,
        "origin": origin.upper() if origin else None,
        "destination": destination.upper() if destination else None,
        "count": len(flights),
        "flights": flights,
    }