from asyncio import sleep

from discord import Status, Activity
from discord.ext.commands import Cog

class Ready(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print(f"-> Clasher Status: Started")
        
        while True:
            await self.client.change_presence(status=Status.dnd, activity=Activity(name="Clash Royale", type=1))
            sleep(30)
            await self.client.change_presence(status=Status.dnd, activity=Activity(name="Type !!help for help", type=3))
            sleep(30)
        
def setup(client):
    client.add_cog(Ready(client))