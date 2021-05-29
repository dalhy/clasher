from discord import Status, Activity
from discord.ext.commands import Cog

class Ready(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print(f"-> Clasher Status: Running...")
        
        await self.client.change_presence(
            status=Status.dnd,
            activity=Activity(
                name="Clash Royale",
                type=1
            )
        )
        
def setup(client):
    client.add_cog(Ready(client))