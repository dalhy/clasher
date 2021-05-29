from traceback import format_exc

from discord import Intents
from discord.ext.commands import Bot

from Source.Utils.Utils import data

client = Bot(
    command_prefix="!!",
    description="Bot to interact with Clash Royale API.",
    intents=Intents.all()
)
client.remove_command("help")

modulos = [
    "Source.Help",
    "Source.Player",
    "Source.Eval",
    "Source.Events.Ready"
]

try:
    for i in modulos:
        client.load_extension(i)
        print(f"-> {i}: Loaded")
except:
    print(f"-> {i} Except: {format_exc()}")
    
try:
    client.run(data["token_bot"])
except Exception as e:
    print(f"-> Clasher: {e}...")