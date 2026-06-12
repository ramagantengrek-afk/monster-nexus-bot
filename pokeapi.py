import aiohttp
import random

BASE_URL = "https://pokeapi.co/api/v2/"

async def get_pokemon_data(name_or_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}pokemon/{name_or_id}") as resp:
            if resp.status == 200:
                return await resp.json()
            return None

async def get_random_pokemon():
    # Ada sekitar 1025 Pokemon saat ini
    pokemon_id = random.randint(1, 1025)
    return await get_pokemon_data(pokemon_id)

def calculate_iv():
    return {
        "hp": random.randint(0, 31),
        "atk": random.randint(0, 31),
        "def": random.randint(0, 31),
        "sp_atk": random.randint(0, 31),
        "sp_def": random.randint(0, 31),
        "speed": random.randint(0, 31)
    }
