from discord import Embed
from discord.ext.commands import Cog, BucketType, command, guild_only, cooldown

from Source.Utils.Utils import data

class Help(Cog):
    def __init__(self, client):
        self.client = client
        
    @command(aliases=["commands", "botinfo"])
    @guild_only()
    @cooldown(1, 5, BucketType.user)
    async def help(self, ctx):
        try:
            embed = Embed(
                color=int(data["color"], 16),
                title=":crossed_swords: Clasher"
            )
                
            embed.add_field(
                name="** Comnands **",
                value=f"{data['emojis']['text']} **help** - Get Help" + "\n" + f"{data['emojis']['text']} **player** - Get a player's information"
            )
                
            embed.add_field(
                name="** News **",
                value=f"{data['emojis']['mega']} No news"
            )
                
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.set_footer(text=ctx.author.name)
                
            await ctx.send(embed=embed)
                
        except Exception as e:
            print(f"-> Help: {e}")
            
def setup(client):
    client.add_cog(Help(client))