import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "playlist-read-private playlist-modify-public playlist-modify-private"


def main():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE
        )
    )

    user_id = sp.current_user()["id"]
    print(f"Usuário autenticado: {user_id}\n")

    offset = 0
    limit = 50
    removidas = 0

    while True:
        playlists = sp.current_user_playlists(limit=limit, offset=offset)
        items = playlists["items"]

        if not items:
            break

        for playlist in items:
            if playlist["owner"]["id"] == user_id:
                sp.current_user_unfollow_playlist(playlist["id"])
                removidas += 1
                print(f"Removida: {playlist['name']}")

        offset += limit

    print(f"\nTotal de playlists removidas: {removidas}")


if __name__ == "__main__":
    main()
