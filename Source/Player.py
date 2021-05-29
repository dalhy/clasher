from requests import get
from asyncio import sleep

from discord import Embed
from discord.ext.commands import Cog, BucketType, command, guild_only, cooldown

from Source.Utils.Utils import Replacer, data

class Player(Cog):
    def __init__(self, client):
        self.client = client
        
    @command()
    @guild_only()
    @cooldown(1, 60, BucketType.user)
    async def player(self, ctx, *, playertag = None):
        try:
            if playertag is None:
                await ctx.send(f"{data['emojis']['error']} Incorrect command usage. Right usage: **player <playertag>**.")
            else:
                message = await ctx.reply(f"{data['emojis']['find']} Looking for information of **{playertag}**...", mention_author=False)
                
                playerformat = str(playertag).replace("#", "%23")
                playerdata = get(f"https://api.clashroyale.com/v1/players/{playerformat}", headers={"Authorization": data["token_api"]}).json()
                playerdata_chest = get(f"https://api.clashroyale.com/v1/players/{playerformat}/upcomingchests", headers={"Authorization": data["token_api"]}).json()
        
                if playerdata.status_code == 404 or playerdata_chest.status_code == 404:
                    return await message.edit(f"{data['emojis']['error']} Player not found. If you haven't your or another player tag, join Clash Royale and copy an player tag.")
        
                #playerdata["totalCards"] = 0
                #playerdata["upcomingChests"] = ""
                
        except Exception as e:
            print(f"-> Player: {e}")
        
        message = await ctx.send("** **")
        try:
            if playertag is not None:                                
                message = await message.edit(content=f"{data['emojis']['find']} Looking for information of **{playertag}**...")
                
                playerformat = str(playertag).replace("#", "%23")
                playerdata = get(f"https://api.clashroyale.com/v1/players/{playerformat}", headers={"Authorization": data["token_api"]}).json()
                playerdata["totalCards"] = 0
                playerdata["upcomingChests"] = ""
                
                playerdata_chest = get(f"https://api.clashroyale.com/v1/players/{playerformat}/upcomingchests", headers={"Authorization": data["token_api"]}).json()
                replacers_chests = {
                    "Wooden Chest": f"{data['emojis']['chests']['wooden_chest']} Wooden Chest",
                    "Silver Chest": f"{data['emojis']['chests']['silver_chest']} Silver Chest",
                    "Golden Chest": f"{data['emojis']['chests']['golden_chest']} Golden Chest",
                    "Giant Chest": f"{data['emojis']['chests']['giant_chest']} Giant Chest",
                    "Epic Chest": f"{data['emojis']['chests']['epic_chest']} Epic Chest",
                    "Magical Chest": f"{data['emojis']['chests']['magical_chest']} Magical Chest",
                    "Legendary Chest": f"{data['emojis']['chests']['legendary_chest']} Legendary Chest",
                    "Mega Lightning Chest": f"{data['emojis']['chests']['megalightning_chest']} Mega Lightning Chest"
                }
                
                for i in playerdata["cards"]:
                    playerdata["totalCards"] = (int(playerdata["totalCards"]) + 1)

                for i in playerdata_chest["items"]:
                    playerdata["upcomingChests"] += "%s **(%s°)**\n" % (i['name'], i['index'] + 1)

                embed = Embed(
                    color=int(data["color"], 16), title=":crossed_swords: Clasher"
                )
                embed.add_field(
                    name="** Profile **",
                    value=f"{data['emojis']['paper']} Name: **{playerdata['name']} ({playerdata['tag']})**" + "\n" + f"{data['emojis']['experience']} Level: **{playerdata['expLevel']}**" + "\n" + f"{data['emojis']['trophy']} Season Trophies: **{playerdata['trophies']} ({playerdata['arena']['name']})**" + "\n" + f"{data['emojis']['special_trophy']} Best Trophies of Season: **{playerdata['bestTrophies']}**" + "\n" + f"{data['emojis']['card']} Total Cards: **{playerdata['totalCards']}/{data['max_cards']}**" + "\n" + f"{data['emojis']['special_card']} Favourite Card: **{playerdata['currentFavouriteCard']['name']}**"
                )
                embed.add_field(
                    name="** Battles **",
                    value=f"{data['emojis']['book']} Battle Count: **{playerdata['battleCount']}**" + "\n" + f"{data['emojis']['swords']} Wins: **{playerdata['wins']}**" + "\n" + f"{data['emojis']['error']} Losses: **{playerdata['losses']}**" + "\n" + f"{data['emojis']['crown']} Three Crown Wins: **{playerdata['threeCrownWins']}**"
                )
                embed.add_field(
                    name="** Challenges & Tournaments **",
                    value=f"{data['emojis']['challenge']} Challenge Max Wins: **{playerdata['challengeMaxWins']}**" + "\n" + f"{data['emojis']['tournament']} Tournament Count: **{playerdata['tournamentBattleCount']}**" + "\n" + f"{data['emojis']['card']} Challenge Cards Won: **{playerdata['challengeCardsWon']}**" + "\n" + f"{data['emojis']['card']} Tournament Cards Won: **{playerdata['tournamentCardsWon']}**"
                )
                
                if "clan" in playerdata:
                    embed.add_field(
                        name="** Clan **",
                        value=f"{data['emojis']['clan']} Name: **{playerdata['clan']['name']} ({playerdata['clan']['tag']})**"
                    )
                
                embed.add_field(
                    name="** Upcoming Chests **",
                    value=f"{Replacer(playerdata['upcomingChests'], replacers_chests)}"
                )
                
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.set_footer(text=ctx.author.name)
                
                await message.edit(content="** **", embed=embed)
                
            else:
                await message.edit(content=f"{data['emojis']['error']} Player not found. If you haven't your or another player tag, join Clash Royale and copy an player tag.")
                
        except Exception as e:
            print(f"-> Player: {e}")
            
            await message.edit(content=f"{data['emojis']['error']} Error. Exception log has emmited.")
"""

def setup(client):
    client.add_cog(Player(client))