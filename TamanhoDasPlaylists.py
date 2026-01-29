import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ================= CONFIGURAÇÃO =================
CLIENT_ID = "<your_client_id>"
CLIENT_SECRET = "<your_client_secret>"
REDIRECT_URI = "http://127.0.0.1:8888/callback"

SCOPE = "playlist-read-private playlist-read-collaborative"

# MB por minuto (estimativas realistas)
QUALITY_MB_PER_MIN = {
    "Baixa (96 kbps)": 0.72,
    "Normal (160 kbps)": 1.20,
    "Alta (320 kbps)": 2.40,
    "Altíssima (512 kbps)": 3.84
}

# ================= AUTENTICAÇÃO =================
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ),
    requests_timeout=30,      # ⬅️ AQUI
    retries=5                 # ⬅️ E AQUI
)


user_id = sp.current_user()["id"]

# ================= FUNÇÕES =================


def get_playlist_duration_minutes(playlist_id):
    total_ms = 0
    offset = 0
    limit = 50

    while True:
        results = sp.playlist_items(
            playlist_id,
            limit=limit,
            offset=offset
        )
        items = results["items"]

        if not items:
            break

        for item in items:
            track = item.get("track")
            if track and track.get("duration_ms"):
                total_ms += track["duration_ms"]

        offset += limit

    return total_ms / 1000 / 60  # ms → minutos


def format_hours(minutes):
    hours = minutes / 60
    return f"{hours:.2f} h"


def get_all_playlists():
    playlists = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        items = results["items"]

        if not items:
            break

        playlists.extend(items)
        offset += limit

    return playlists


# ================= PROCESSAMENTO =================
playlists = get_all_playlists()

print("\n📦 ESTIMATIVA DE TAMANHO DE DOWNLOAD (BASEADO EM DURAÇÃO REAL)\n")

for playlist in playlists:
    name = playlist["name"]
    playlist_id = playlist["id"]

    duration_min = get_playlist_duration_minutes(playlist_id)
    duration_h = format_hours(duration_min)

    print(f"🎧 Playlist: {name}")
    print(f"⏱️ Duração total: {duration_h}")

    for quality, mb_per_min in QUALITY_MB_PER_MIN.items():
        size_mb = duration_min * mb_per_min
        size_gb = size_mb / 1024
        print(f"   • {quality}: {size_gb:.2f} GB")

    print("-" * 50)

print("\n✔ Análise concluída.")
