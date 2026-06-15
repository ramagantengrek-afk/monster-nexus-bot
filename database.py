import sqlite3
import os
try:
    from config import DB_PATH
except ImportError:
    from ..config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabel Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        active_pokemon_id INTEGER,
        pokedex_count INTEGER DEFAULT 0
    )
    ''')
    
    # Tabel Pokemons
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pokemons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER,
        species_id INTEGER,
        name TEXT,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        hp_iv INTEGER, atk_iv INTEGER, def_iv INTEGER,
        sp_atk_iv INTEGER, sp_def_iv INTEGER, speed_iv INTEGER,
        is_shiny INTEGER DEFAULT 0,
        FOREIGN KEY (owner_id) REFERENCES users(user_id)
    )
    ''')
    
    # Tabel Guilds (untuk spawn channel)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY,
        spawn_channel_id INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Jalankan inisialisasi saat modul dimuat
init_db()
