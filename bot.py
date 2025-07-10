import discord
from discord.ext import commands
from api import AternosAPI
import secretos
import json
import os
import random
import requests

# Configura tus credenciales
headers_cookie = "ATERNOS_SESSION=AuXbFYGj5SmDWJ6L2JdX7dm2wfONUwDC3K6xxoQ3e1KTU4oJQcPdFAsPZ0FM4pV2zZDbJXMchhu548jmIR2O8YP7RWdIdF4Ubxdm; ATERNOS_SEC_xxxxx=yyyyy; ATERNOS_SERVER=84jkIui0VIWl9vQ6"
aternos = AternosAPI(headers_cookie, secretos.TOKEN)

# Define the bot prefix and intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Define the target user ID
TARGET_USER_ID = 689129289001730093

FRASES_FILE = "./frases.json"



def get_random_gif():
    # Example using Tenor API (replace 'YOUR_TENOR_API_KEY' with your actual API key)
    search_term = "funny"
    url = f"https://g.tenor.com/v1/random?q={search_term}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        gifs = response.json().get("results", [])
        if gifs:
            return gifs[0].get("media")[0].get("gif").get("url")
    return None

def get_random_phrase():
    # Lista de frases aleatorias
    phrases = [
        "¿Ya tomaste la leche?",
        "Siempre hay GDV <3",
        "Toma esta frase motivadora: ¡Nunca te rindas, los sueños se cumplen!",
        "Toma esta frase motivadora: ¡El éxito es la suma de pequeños esfuerzos repetidos día tras día!",
        "Toma esta frase motivadora: ¡La vida es un 10% lo que te ocurre y un 90% cómo reaccionas!"
    ]
    return random.choice(phrases)

def get_random_phrase_from_file():
    with open("frases.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return random.choice(data)["frase"]

def save_last_user_id(user_id):
    with open("ids.json", "r+", encoding="utf-8") as file:
        data = json.load(file)
        # Update or add the last user ID
        data.append({"last_user_id": user_id})
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.truncate()

def save_user_id(user_id):
    ids_file = "ids.json"
    if not os.path.exists(ids_file):
        with open(ids_file, "w", encoding="utf-8") as file:
            json.dump({}, file)

    with open(ids_file, "r+", encoding="utf-8") as file:
        data = json.load(file)
        if str(user_id) not in data:
            data[str(user_id)] = {"messages_count": 1}
        else:
            data[str(user_id)]["messages_count"] += 1
        file.seek(0)
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.truncate()

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Save the ID of the user who sent the message
    save_user_id(message.author.id)
    
    # Check if the message is from the target user
    if message.author.id == TARGET_USER_ID:
        phrase = get_random_phrase_from_file()
        embed = discord.Embed(
            title="Frase del día 🌟",
            description=phrase,
            color=discord.Color.blue()
        )
        embed.set_footer(text="Siempre hay GDV 💙")
        await message.channel.send(embed=embed)
    else:
        # Process other commands/messages
        await bot.process_commands(message)


bot.remove_command('help')

if __name__ == "__main__":
    bot.run(secretos.TOKEN)
