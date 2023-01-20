import discord
from discord import app_commands
from discord.ext import commands
from musicbot.commands import music

class Extra(commands.Cog):
    """ A collection of extra commands for the bot in your server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rocknroll", description="Plays the Rock NZ")
    async def rocking(self, ctx:discord.Interaction): # dest_channel_name: str
        self.bot.get_cog('Music')._play_song(ctx, "https://icecast.mediaworks.nz/rock_128kbps")


async def setup(bot):
    await bot.add_cog(Extra(bot))