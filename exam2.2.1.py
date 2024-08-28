import asyncio
import aiohttp
import time
from datetime import datetime

async def fetch_pokemon_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_pokemon_with_ability(url):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        data = await fetch_pokemon_data(session, url)
        duration = time.time() - start_time
        pokemon_names = [p['pokemon']['name'] for p in data.get('pokemon', [])]
        return len(pokemon_names), pokemon_names, duration

def format_duration(seconds):
    return f"{seconds:.2f} seconds"

def format_time():
    return datetime.now().strftime("%a %b %d %Y %H:%M:%S")  

async def main():
    urls = {
        "battle-armor": "https://pokeapi.co/api/v2/ability/battle-armor",
        "speed-boost": "https://pokeapi.co/api/v2/ability/speed-boost"
    }
    results = await asyncio.gather(
        get_pokemon_with_ability(urls["battle-armor"]),
        get_pokemon_with_ability(urls["speed-boost"])
    )
    
    for ability, result in zip(urls.keys(), results):
        count, names, duration = result
        print(f"[{format_time()}] There are {count} Pokémon with the '{ability}' ability.")
        print("The Pokémon are:")
        print(names)
        print(f"Time taken: {format_duration(duration)}\n")

asyncio.run(main())
