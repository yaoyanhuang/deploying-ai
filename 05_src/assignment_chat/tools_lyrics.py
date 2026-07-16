import requests
from urllib.parse import quote
from langchain.tools import tool
import json

@tool
def get_lyrics(title:str, artist: str, timeout: int = 10) -> str | None:
    """
    Retrieve song lyrics from the Lyrics.ovh API.

    Args:
        artist: Artist name.
        title: Song title.
        timeout: Request timeout in seconds.

    Returns:
        The lyrics as a string if found, otherwise None.
    """
    artist = quote(artist.strip())
    title = quote(title.strip())

    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        return data.get("lyrics")

    except requests.exceptions.HTTPError:
        print(f"Lyrics not found for '{title}' by '{artist}'.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None
    