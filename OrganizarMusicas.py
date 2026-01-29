import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import time

# ========================
# CONFIGURAÇÕES
# ========================
CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "user-library-read user-top-read user-read-recently-played playlist-modify-private"

# ========================
# AUTENTICAÇÃO
# ========================
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
)

user_id = sp.current_user()["id"]
print(f"Usuário autenticado: {user_id}")

# ========================
# FUNÇÕES AUXILIARES
# ========================


def chunks(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def create_playlist(name):
    return sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False,
        description="Gerada automaticamente por script"
    )["id"]


def flush(playlist_id, buffer):
    for batch in chunks(buffer, 100):
        sp.playlist_add_items(playlist_id, batch)
        time.sleep(1)  # pausa segura
    buffer.clear()


# ========================
# 1️⃣ TOP TRACKS (GOSTO REAL)
# ========================
top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")
top_track_ids = {t["id"] for t in top_tracks["items"]}

# ========================
# 2️⃣ RECENTLY PLAYED
# ========================
recent = sp.current_user_recently_played(limit=50)
recent_ids = {i["track"]["id"] for i in recent["items"]}

# ========================
# 3️⃣ GÊNEROS DOMINANTES (BATCH)
# ========================
artist_ids = set()
for t in top_tracks["items"]:
    for a in t["artists"]:
        artist_ids.add(a["id"])

all_genres = []

for batch in chunks(list(artist_ids), 50):
    artists_batch = sp.artists(batch)["artists"]
    for artist in artists_batch:
        all_genres.extend(artist["genres"])

genres_counter = Counter(all_genres)
top_genres = {g for g, _ in genres_counter.most_common(10)}

print("Gêneros dominantes:", top_genres)

# ========================
# 4️⃣ CRIAR PLAYLISTS
# ========================
pl_priority = create_playlist("DOWNLOAD_PRIORITARIO")
pl_similar = create_playlist("DOWNLOAD_PARECIDO")
pl_skip = create_playlist("NAO_BAIXAR")

# ========================
# 5️⃣ CACHE DE ARTISTAS
# ========================
artist_genre_cache = {}


def get_artist_genres(artist_ids):
    missing = [a for a in artist_ids if a not in artist_genre_cache]

    for batch in chunks(missing, 50):
        artists = sp.artists(batch)["artists"]
        for artist in artists:
            artist_genre_cache[artist["id"]] = set(artist["genres"])

    genres = set()
    for a in artist_ids:
        genres.update(artist_genre_cache.get(a, set()))

    return genres


# ========================
# 6️⃣ PROCESSAR CURTIDAS (SEM RATE-LIMIT)
# ========================
buffer_priority = []
buffer_similar = []
buffer_skip = []

offset = 0
limit = 50

while True:
    liked = sp.current_user_saved_tracks(limit=limit, offset=offset)
    if not liked["items"]:
        break

    for item in liked["items"]:
        track = item["track"]
        if not track or not track["id"]:
            continue

        track_id = track["id"]
        track_artist_ids = [a["id"] for a in track["artists"]]
        track_genres = get_artist_genres(track_artist_ids)

        if track_id in top_track_ids or track_id in recent_ids:
            buffer_priority.append(track_id)
        elif track_genres & top_genres:
            buffer_similar.append(track_id)
        else:
            buffer_skip.append(track_id)

    # envia em lote a cada página
    flush(pl_priority, buffer_priority)
    flush(pl_similar, buffer_similar)
    flush(pl_skip, buffer_skip)

    offset += limit

print("Organização concluída com sucesso.")
