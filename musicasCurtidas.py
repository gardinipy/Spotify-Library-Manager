import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# ===== CONFIGURAÇÃO =====
CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = 'user-library-read playlist-modify-public playlist-modify-private'

PLAYLIST_NAME = 'Minhas músicas curtidas'
PLAYLIST_DESC = 'Todas as músicas curtidas por mim (sincronizada automaticamente)'

# ===== AUTH =====
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
)

user_id = sp.current_user()['id']

# ===== ENCONTRAR OU CRIAR PLAYLIST =====


def get_or_create_playlist():
    playlists = sp.current_user_playlists(limit=50)

    for pl in playlists['items']:
        if pl['name'].lower() == PLAYLIST_NAME.lower():
            print('Playlist encontrada. Atualizando...')
            return pl['id']

    print('Playlist não encontrada. Criando nova...')
    playlist = sp.user_playlist_create(
        user=user_id,
        name=PLAYLIST_NAME,
        public=True,
        description=PLAYLIST_DESC
    )
    return playlist['id']


playlist_id = get_or_create_playlist()

# ===== LIMPAR PLAYLIST (UPDATE REAL) =====
sp.playlist_replace_items(playlist_id, [])
time.sleep(1)

# ===== COPIAR CURTIDAS =====
limit = 50
offset = 0

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    items = results['items']

    if not items:
        break

    track_uris = [
        item['track']['uri']
        for item in items
        if item.get('track')
    ]

    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        time.sleep(1)

    offset += limit

print('Playlist sincronizada com sucesso.')
