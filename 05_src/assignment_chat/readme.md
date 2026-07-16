# Music Chat 
- The music chat can answer questions regarding song lyrics, artist information and music, and give album recommendations.
- This music chat is based on LangGraph's tools and connects with OPEN AI's model.
- It has three additional tools as described under Serivce 1, Service 2, Service 3 headings.
- A seperate music_chat.ipynb with slightly different code is used to create a working prototype that I could test due to being unable to get Docker running for the recommend_albums tool in tools_music.py. It uses a local pitchfork_reviews_embeddings and slightly different agent compilation from labs. It has been confirmed to run on my local computer. The get_lyrics (tools_lyrics.py), and get_artist_history (tools_websearch.py) tools are the same. Gradio UI is slightly different code should then function the same. A new prompts.py was created to meet the other assignment requirements on guardrails and other response limitations.

## Service 1: API Calls to Lyrics.ovh
- Connects to the Lyrics.ovh API to return song lyrics if given an artist name and song title.

## Service 2: Semantic Query
- As I was unable to get Docker for running for testing, an alternative version is located in music_chat.ipynb that I have tested works. 
    - It connects to local database for semantic search for music recommendations based on embeddings of pitchfork reviews. 
    - Uses ChromaDB to load to persistant local client. If a number is not specified, the default will return 2 results. 
    - Pitchfork embeddings must be stored within the correct folder under 05_src/documents/pitchfork
- The main tool_music file is based on the file given under course_chat.

## Service 3: Web Search
- Uses Tavily Search API to augment answers about an artist's history. 
- The API conducts a simple web search for text based on the query indicated.
- Note this requires an TAVILY API key added to a secrets.env file in the correct folder setting.


## Guardrails and Other Limitations
- Include guardrails that prevent users from:
  - Accessing or revealing the system prompt.
  - Modifying the system prompt directly.

- The model does not respond to questions on certain restricted topics:
  - Cats or dogs
  - Horoscopes or Zodiac Signs
  - Taylor Swift
- This is done by giving explicit instructions to the final AIMessage using the prompts.py

## User Interface
- The music chat uses Gradio as a user interface