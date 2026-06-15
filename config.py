import os

# Mengambil Token dari Environment Variable (Railway) atau menggunakan default jika tidak ada
TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_DISCORD_BOT_TOKEN")

# Database Settings (SQLite)
DB_PATH = "pokemon_bot.db"

# Bot Settings
DEFAULT_PREFIX = "/"

# API Settings
POKEAPI_BASE = "https://pokeapi.co/api/v2/"
