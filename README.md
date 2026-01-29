# 🎧 Spotify Library Manager (Python)

Conjunto de scripts em Python para **gerenciar, organizar e analisar bibliotecas do Spotify** usando **exclusivamente a API oficial**.

Este repositório foi criado para resolver problemas reais de quem possui:
- milhares de músicas curtidas
- muitas playlists acumuladas
- limitação de armazenamento para download offline
- necessidade de organização automatizada

⚠️ Nenhum script realiza download de músicas nem viola os Termos de Uso do Spotify.

---

## 📂 Scripts disponíveis

### 1️⃣ `musicasCurtidas.py`
Sincroniza suas **Músicas Curtidas** em uma playlist dedicada.

**O que faz:**
- Cria a playlist *“Minhas músicas curtidas”* se não existir
- Atualiza a playlist se já existir (não duplica)
- Mantém a playlist sempre igual ao estado atual das curtidas

**Uso típico:**
- Backup lógico das curtidas
- Base para downloads offline
- Fonte única para organização posterior

---

### 2️⃣ `OrganizarMusicas.py`
Organização inteligente das músicas curtidas com base em **comportamento real**.

**Critérios utilizados:**
- Top Tracks (o que você mais ouve)
- Recently Played (o que você escuta atualmente)
- Gêneros dominantes do perfil

**Cria automaticamente:**
- `DOWNLOAD_PRIORITARIO`
- `DOWNLOAD_PARECIDO`
- `NAO_BAIXAR`

Ideal para reduzir milhares de músicas a um conjunto realmente útil para download.

---

### 3️⃣ `TamanhoDasPlaylists.py`
Analisa **todas as playlists** e calcula o **tamanho estimado de download** com base na **duração real das faixas**.

**Estimativas de qualidade:**
- Baixa (96 kbps)
- Normal (160 kbps)
- Alta (320 kbps)
- Altíssima (512 kbps)

**Resultado:**
- Duração total da playlist (em horas)
- Tamanho estimado em GB para cada qualidade
- Planejamento realista de armazenamento offline

---

### 4️⃣ `apagarPlaylist.py`
Remove (unfollow) playlists criadas pelo usuário.

**Importante:**
- O Spotify não permite exclusão real via API
- “Excluir” no app equivale a **unfollow**
- Este script replica exatamente esse comportamento oficial

Útil para:
- limpeza de playlists antigas
- reset de ambiente
- automação de higiene da biblioteca

---

## 🔐 Requisitos

- Python 3.9+
- Conta Spotify (Free ou Premium)
- App criado em: https://developer.spotify.com/dashboard

### Dependência
```bash
pip install spotipy
