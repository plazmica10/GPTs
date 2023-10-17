
import openai
import spotipy
import pprint
import argparse
import json
from dotenv import dotenv_values

config = dotenv_values("../.env")

def main():
    openai.api_key = config["AIKEY"]
    #command line arguments for prompt and number of songs
    parser = argparse.ArgumentParser(description="Simple command line playlist utility")
    parser.add_argument("-p", type=str, default = "90's songs", help="The prompt to describing the playlist.")
    parser.add_argument("-n", type=int, default="8", help="The number of songs to be added.")
    args = parser.parse_args()

    playlist = get_playlist(args.p, args.n)
    add_songs_to_spotify(args.p, playlist)

#request playlist from openai
def get_playlist(prompt, count=8):
    example_json = """
    [
      {"song": "Everybody Hurts", "artist": "R.E.M."},
      {"song": "Nothing Compares 2 U", "artist": "Sinead O'Connor"},
      {"song": "Tears in Heaven", "artist": "Eric Clapton"},
      {"song": "Hurt", "artist": "Johnny Cash"},
      {"song": "Yesterday", "artist": "The Beatles"}
    ]
    """
    messages = [
        {"role": "system", "content": """You are a helpful playlist generating assistant. 
        You should generate a list of songs and their artists according to a text prompt.
        Your should return a JSON array, where each element follows this format: {"song": <song_title>, "artist": <artist_name>}
        """
        },
        {"role": "user", "content": "Generate a playlist of 5 songs based on this prompt: super super sad songs"},
        {"role": "assistant", "content": example_json},
        {"role": "user", "content": f"Generate a playlist of {count} songs based on this prompt: {prompt}"},
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=400
    )

    playlist = json.loads(response["choices"][0]["message"]["content"])
    return playlist

def add_songs_to_spotify(prompt, playlist):
    #first authenticate with spotify
    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOTIFY_CLIENT_ID"],
            client_secret=config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://localhost:3001",
            scope="playlist-modify-private",
        )
    )
    #get current user 
    current_user = sp.current_user()
    assert current_user is not None

    tracks = []
    #search for each song on Spotify and add to list
    for item in playlist:
        artist,song = item["artist"],item["song"]
        query = f"{artist} {song}"
        result = sp.search(q=query, type="track", limit=10)
        tracks.append(result["tracks"]["items"][0]["id"])

    #create playlist
    created_playlist = sp.user_playlist_create(
        current_user["id"],
        public=False,
        name=prompt
    )
    #add songs to playlist
    sp.user_playlist_add_tracks(current_user["id"], created_playlist["id"], tracks)

if __name__ == "__main__":
    main()

