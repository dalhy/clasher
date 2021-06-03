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
            await self.client.change_presence(activity=Activity(name="Clash Royale", type=0))
            await sleep(30)
            await self.client.change_presence(activity=Activity(name="Type !!help for help", type=2))
            await sleep(30)
        
def setup(client):
    client.add_cog(Ready(client))