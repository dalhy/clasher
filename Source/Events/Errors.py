from sys import stderr
from traceback import print_exc

from discord.ext.commands import Cog, CommandOnCooldown, MissingPermissions, BotMissingPermissions, NotOwner

from Source.Utils.Utils import data

class Errors(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
    
        if isinstance(error, CommandOnCooldown):
            if int(error.retry_after) < 60:
                return await ctx.reply(f"{data['emojis']['clock']} Await **{int(error.retry_after) % 60}s** to use this command again.")
            elif int(error.retry_after) < 3600: 
                return await ctx.reply(f"{data['emojis']['clock']} Await **{int(int(error.retry_after) / 60)}m** and **{int(error.retry_after) % 60}s** to use this command again.")
            
        if isinstance(error, MissingPermissions):
            perms = "\n".join(error.missing_perms)
            return await ctx.reply(f"{data['emojis']['error']} To execute this command, you need the following permissions: **{perms}**.")
            
        if isinstance(error, BotMissingPermissions):
            perms = "\n".join(error.missing_perms)
            return await ctx.reply(f"{data['emojis']['error']} To execute this command, I need the following permissions: **{perms}**.")
            
        if isinstance(error, NotOwner):
            return await ctx.send(f"{data['emojis']['error']} Only my **owner** can use this command.")
                
        print_exc(type(error), error, error.__traceback__, file=stderr)
        
def setup(client):
    client.add_cog(Errors(client))