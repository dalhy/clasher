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
                request_playerdata = get(f"https://api.clashroyale.com/v1/clans/{clanformat}", headers={"Authorization": data["token_api"]})
                request_playerdata_chest = get(f"https://api.clashroyale.com/v1/players/{playerformat}/upcomingchests", headers={"Authorization": data["token_api"]})
        
                playerdata = request_playerdata.json()
                playerdata_chest = request_playerdata_chest.json()
        
                if request_playerdata.status_code == 404 or request_playerdata_chest.status_code == 404:
                    ctx.command.reset_cooldown(ctx)
                    await message.edit(content=f"{data['emojis']['error']} Player not found. If you havent your or another player tag, join Clash Royale and copy an player tag.")
                else:
                    playerdata["totalCards"] = 0
                    playerdata["upcomingChests"] = ""
                
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
                        playerdata["upcomingChests"] += "%s **(%s°)**\n" % (i["name"], i["index"] + 1)
                
                    embed = Embed(
                        color=int(data["color"], 16),
                        title=":crossed_swords: Clasher"
                    )
                    embed.add_field(
                        inline=False,
                        name="** Profile **",
                        value=f"{data['emojis']['paper']} Name: **{playerdata['name']} ({playerdata['tag']})**" + "\n" + f"{data['emojis']['experience']} Level: **{playerdata['expLevel']}**" + "\n" + f"{data['emojis']['trophy']} Season Trophies: **{playerdata['trophies']} ({playerdata['arena']['name']})**" + "\n" + f"{data['emojis']['special_trophy']} Best Trophies of Season: **{playerdata['bestTrophies']}**" + "\n" + f"{data['emojis']['card']} Total Cards: **{playerdata['totalCards']}/{data['max_cards']}**" + "\n" + f"{data['emojis']['special_card']} Favourite Card: **{playerdata['currentFavouriteCard']['name']}**"
                    )
                    embed.add_field(
                        inline=False,
                        name="** Battles **",
                        value=f"{data['emojis']['book']} Battle Count: **{playerdata['battleCount']}**" + "\n" + f"{data['emojis']['swords']} Wins: **{playerdata['wins']}**" + "\n" + f"{data['emojis']['error']} Losses: **{playerdata['losses']}**" + "\n" + f"{data['emojis']['crown']} Three Crown Wins: **{playerdata['threeCrownWins']}**"
                    )
                    embed.add_field(
                        inline=False,
                        name="** Challenges & Tournaments **",
                        value=f"{data['emojis']['challenge']} Challenge Max Wins: **{playerdata['challengeMaxWins']}**" + "\n" + f"{data['emojis']['tournament']} Tournament Count: **{playerdata['tournamentBattleCount']}**" + "\n" + f"{data['emojis']['card']} Challenge Cards Won: **{playerdata['challengeCardsWon']}**" + "\n" + f"{data['emojis']['card']} Tournament Cards Won: **{playerdata['tournamentCardsWon']}**"
                    )
                                    
                    if "clan" in playerdata:
                        embed.add_field(
                            inline=False,
                            name="** Clan **",
                            value=f"{data['emojis']['clan']} Name: **{playerdata['clan']['name']} ({playerdata['clan']['tag']})**"
                        )
                                    
                    embed.add_field(
                        inline=False,
                        name="** Upcoming Chests **",
                        value=f"{Replacer(playerdata['upcomingChests'], replacers_chests)}"
                    )
                                    
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=ctx.author.name)
                    
                    await message.edit(content="** **", embed=embed)
                
        except Exception as e:
            print(f"-> Clan: {e}")

def setup(client):
    client.add_cog(Clan(client))