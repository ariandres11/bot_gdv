import discord
from discord.ext import commands
import secretos
import json
import os
import random



# Define the bot prefix and intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Define the target user ID
TARGET_USER_ID = 689129289001730093

FRASES_FILE = "./frases_rodri.json"

def get_rodri_phrase():
    if not os.path.exists(FRASES_FILE):
        return "No hay frases filosóficas aún."
    with open(FRASES_FILE, "r", encoding="utf-8") as file:
        frases = json.load(file)
        if frases:
            return random.choice(frases)
        else:
            return "No hay frases filosóficas aún."

def add_rodri_phrase(frase):
    frases = []
    if os.path.exists(FRASES_FILE):
        with open(FRASES_FILE, "r", encoding="utf-8") as file:
            frases = json.load(file)
    frases.append(frase)
    with open(FRASES_FILE, "w", encoding="utf-8") as file:
        json.dump(frases, file, ensure_ascii=False, indent=2)

SALUDOS = ["hola", "hello", "hi", "buenas", "holi", "holis", "saludos", "qué tal", "que tal"]

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Saludo personalizado
    if any(saludo in message.content.lower() for saludo in SALUDOS):
        await message.channel.send("hola gil que querés")
        return

    # Comando $rodri para frase filosófica
    if message.content.strip().lower().startswith("$rodri"):
        frase = get_rodri_phrase()
        await message.channel.send(f"Rodri dice: {frase}")
        return

    # Comando para agregar frase: $addrodri tu frase aquí
    if message.content.strip().lower().startswith("$addrodri"):
        nueva_frase = message.content[len("$addrodri"):].strip()
        if nueva_frase:
            add_rodri_phrase(nueva_frase)
            await message.channel.send("Frase filosófica agregada.")
        else:
            await message.channel.send("Por favor, escribe una frase para agregar.")
        return

    # Guardar usuario y responder con frase motivadora si es el target
    save_user_id(message.author.id)
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
        await bot.process_commands(message)

bot.remove_command('help')

if __name__ == "__main__":
    bot.run(secretos.TOKEN)
