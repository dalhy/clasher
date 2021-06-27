from requests import get
from asyncio import sleep

from discord import Embed
from discord.ext.commands import Cog, BucketType, command, guild_only, cooldown

from Source.Utils.Utils import Replacer, data

class Clan(Cog):
    def __init__(self, client):
        self.client = client
        
    @command()
    @guild_only()
    @cooldown(1, 20, BucketType.user)
    async def clan(self, ctx, *, clantag = None):
        try:
            if clantag is None:
                ctx.command.reset_cooldown(ctx)
                await ctx.reply(f"{data['emojis']['error']} Incorrect command usage. Right usage: **clan <clantag>**.")
            else:
                message = await ctx.reply(f"{data['emojis']['find']} Looking for information of **{clantag}**...")
                
                clanformat = str(clantag).replace("#", "%23")
                request_clandata = get(f"https://api.clashroyale.com/v1/clans/{clanformat}", headers={"Authorization": data["token_api"]})
                #request_clandata_war = get(f"https://api.clashroyale.com/v1/players/{playerformat}/upcomingchests", headers={"Authorization": data["token_api"]})
        
                clandata = request_clandata.json()
                #clandata_war = request_clandata_war.json()
        
                if request_clandata.status_code == 404:
                    ctx.command.reset_cooldown(ctx)
                    await message.edit(content=f"{data['emojis']['error']} Clan not found. If you havent your clan tag or another clan tag, join Clash Royale and copy one.")
                else:
                    embed = Embed(
                        color=int(data["color"], 16),
                        title=":crossed_swords: Clasher"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['clan']} Clan**",
                        value=f"```\nName: {clandata['name']}" + "\n" + f"Tag: {clandata['tag']}" + "\n" + f"Location: {clandata['location']['name']} ({clandata['location']['countryCode']})" + "\n" + f"Type: {str(clandata['type']).title()}" + "\n" + f"Score {clandata['clanScore']}" + "\n" + f"Members: {clandata['members']}" + "\n" + f"Description: {clandata['description']}```"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['clan_trophy']} Trophies**",
                        value=f"```\nWar Trophies: {clandata['clanWarTrophies']}```"
                    )
                                                        
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=ctx.author.name)
                                        
                    await message.edit(content=" ", embed=embed)
                    
        except Exception as e:
            print(f"-> Clan: {e}")

def setup(client):
    client.add_cog(Clan(client))