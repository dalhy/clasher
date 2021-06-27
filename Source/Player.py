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
    @cooldown(1, 20, BucketType.user)
    async def player(self, ctx, *, playertag = None):
        try:
            if playertag is None:
                ctx.command.reset_cooldown(ctx)
                await ctx.reply(f"{data['emojis']['error']} Incorrect command usage. Right usage: **player <playertag>**.")
            else:
                message = await ctx.reply(f"{data['emojis']['find']} Looking for information of **{playertag}**...")
                
                playerformat = str(playertag).replace("#", "%23")
                request_playerdata = get(f"https://api.clashroyale.com/v1/players/{playerformat}", headers={"Authorization": data["token_api"]})
                request_playerdata_chest = get(f"https://api.clashroyale.com/v1/players/{playerformat}/upcomingchests", headers={"Authorization": data["token_api"]})
        
                playerdata = request_playerdata.json()
                playerdata_chest = request_playerdata_chest.json()
        
                if request_playerdata.status_code == 404 or request_playerdata_chest.status_code == 404:
                    ctx.command.reset_cooldown(ctx)
                    await message.edit(content=f"{data['emojis']['error']} Player not found. If you havent your or another player tag, join Clash Royale and copy one.")
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
                        playerdata["upcomingChests"] += "%s (%s°)\n" % (i["name"], i["index"] + 1)
                
                    embed = Embed(
                        color=int(data["color"], 16),
                        title=":crossed_swords: Clasher"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['paper']} Profile**",
                        value=f"```\nName: {playerdata['name']}" + "\n" + f"Tag: {playerdata['tag']}" + "\n" + f"Level: {playerdata['expLevel']}" + "\n" + f"Total Cards: {playerdata['totalCards']}/{data['max_cards']}" + "\n" + f"Favourite Card: {playerdata['currentFavouriteCard']['name']}```"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['trophy']} Trophies**",
                        value=f"```\nSeason Trophies: {playerdata['trophies']} ({playerdata['arena']['name']})" + "\n" + f"Best Trophies of Season: {playerdata['bestTrophies']}```"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['swords']} Battles**",
                        value=f"```\nBattle Count: {playerdata['battleCount']}" + "\n" + f"Wins: {playerdata['wins']}" + "\n" + f"Three Crown Wins: {playerdata['threeCrownWins']}" + "\n" + f"Losses: {playerdata['losses']}```"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['challenge']} Challenges**",
                        value=f"```\nChallenge Max Wins: {playerdata['challengeMaxWins']}" + "\n" + f"Challenge Cards Won: {playerdata['challengeCardsWon']}```"
                    )
                    embed.add_field(
                        inline=False,
                        name=f"**{data['emojis']['tournament']} Tournaments**",
                        value=f"```\nTournament Count: {playerdata['tournamentBattleCount']}" + "\n" + f"Tournament Cards Won: {playerdata['tournamentCardsWon']}```"
                    )
                                    
                    if "clan" in playerdata:
                        embed.add_field(
                            inline=False,
                            name=f"**{data['emojis']['clan']} Clan**",
                            value=f"```\nName: {playerdata['clan']['name']}" + "\n" + f"Tag: {playerdata['clan']['tag']}" + "\n" + f"Cards Donations: {playerdata['donations']}" + "\n" + f"Cards Donations Received: {playerdata['donationsReceived']}```"
                        )
                                    
                    embed.add_field(
                        inline=False,
                        name=" Upcoming Chests ",
                        value=f"{Replacer(playerdata['upcomingChests'], replacers_chests)}"
                    )
                                    
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.set_footer(text=ctx.author.name)
                    
                    await message.edit(content=" ", embed=embed)
                
        except Exception as e:
            print(f"-> Player: {e}")

def setup(client):
    client.add_cog(Player(client))