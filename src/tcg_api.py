"""
Pokémon TCG API client module.

This module provides functions to fetch Pokémon Trading Card Game data
from the official Pokémon TCG API (https://pokemontcg.io/).
"""
import json
import os

import requests

BASE_URL = "https://api.pokemontcg.io/v2"


def _get_api_key():
    """Get the Pokémon TCG API key from environment.

    Returns:
        str: The API key if available, empty string otherwise.
    """
    return os.getenv("POKEMON_TCG_API_KEY", "")


def _make_request(endpoint, params=None):
    """Make a GET request to the Pokémon TCG API.

    Args:
        endpoint (str): The API endpoint path (e.g., "/cards").
        params (dict, optional): Query parameters for the request.

    Returns:
        dict: Parsed JSON response data, or error dict on failure.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    api_key = _get_api_key()
    if api_key:
        headers["X-Api-Key"] = api_key

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_card_info(card_name):
    """Fetch information about a Pokémon TCG card by name.

    Args:
        card_name (str): The name of the card to search for.

    Returns:
        str: JSON-formatted card details including name, set, rarity,
            type, HP, attacks, abilities, and image URL. Returns an
            error message if card not found.
    """
    params = {"q": f"name:{card_name}"}
    data = _make_request("/cards", params=params)

    if "error" in data:
        return f"Error fetching card info: {data['error']}"

    if not data.get("data"):
        return f"No card found for '{card_name}'"

    card = data["data"][0]  # Take the first match
    attacks = card.get("attacks", [])
    abilities = card.get("abilities", [])

    info = {
        "name": card.get("name"),
        "set": card.get("set", {}).get("name"),
        "rarity": card.get("rarity"),
        "types": card.get("types", []),
        "hp": card.get("hp"),
        "attacks": [
            {"name": attack.get("name"), "damage": attack.get("damage")}
            for attack in attacks
        ],
        "abilities": [
            {"name": ability.get("name"), "text": ability.get("text")}
            for ability in abilities
        ],
        "image": card.get("images", {}).get("small"),
    }
    return json.dumps(info, indent=2)


def get_sets():
    """Fetch all Pokémon TCG expansion sets.

    Returns:
        str: JSON-formatted list of sets with name and release date.
            Returns an error message if request fails.
    """
    data = _make_request("/sets")

    if "error" in data:
        return f"Error fetching sets: {data['error']}"

    sets = [
        {
            "name": set_info["name"],
            "releaseDate": set_info.get("releaseDate"),
        }
        for set_info in data.get("data", [])
    ]
    return json.dumps(sets, indent=2)


def get_most_recent_set():
    """Get the most recent Pokémon TCG expansion set.

    Returns:
        str: JSON-formatted set information with name and release date.
            Returns an error message if request fails or no sets found.
    """
    params = {"orderBy": "-releaseDate", "pageSize": 1}
    data = _make_request("/sets", params=params)

    if "error" in data:
        return f"Error fetching most recent set: {data['error']}"

    if not data.get("data"):
        return "No sets found"

    set_info = data["data"][0]
    result = {
        "name": set_info["name"],
        "releaseDate": set_info.get("releaseDate"),
    }
    return json.dumps(result, indent=2)
