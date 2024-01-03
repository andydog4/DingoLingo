import discord
from config import config
from discord.ext import commands
from discord.ext.commands import has_permissions
from musicbot import utils
from discord import app_commands
from musicbot.audiocontroller import AudioController
from musicbot.utils import guild_to_audiocontroller, guild_to_settings


class General(commands.Cog):
    """ A collection of the commands for moving the bot around in you server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    # logic is split to uconnect() for wide usage
    @app_commands.command(name='connect', description=config.HELP_CONNECT)
    @app_commands.guild_only
    async def _connect(self, ctx):  # dest_channel_name: str
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.uconnect(ctx)

    @app_commands.command(name='disconnect', description=config.HELP_DISCONNECT)
    @app_commands.guild_only
    async def _disconnect(self, ctx, guild=False):
        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        await audiocontroller.udisconnect()

    @app_commands.command(name='reset', description=config.HELP_DISCONNECT)
    @app_commands.guild_only
    async def _reset(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Connected to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @app_commands.command(name='changechannel', description=config.HELP_CHANGECHANNEL)
    @app_commands.guild_only
    async def _change_channel(self, ctx):
        current_guild = utils.get_guild(self.bot, ctx)

        vchannel = await utils.is_connected(ctx)
        if vchannel == ctx.author.voice.channel:
            await ctx.send("{} Already connected to {}".format(":white_check_mark:", vchannel.name))
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await current_guild.voice_client.disconnect(force=True)

        guild_to_audiocontroller[current_guild] = AudioController(
            self.bot, current_guild)
        await guild_to_audiocontroller[current_guild].register_voice_channel(ctx.author.voice.channel)

        await ctx.send("{} Switched to {}".format(":white_check_mark:", ctx.author.voice.channel.name))

    @app_commands.command(name='ping', description=config.HELP_PING)
    @app_commands.guild_only
    async def _ping(self, ctx):
        await ctx.send("Pong")

    @app_commands.command(name='setting', description=config.HELP_SHUFFLE)
    @app_commands.guild_only
    @commands.is_owner
    @commands.has_permissions(administrator=True)
    async def _settings(self, ctx, *args):

        sett = guild_to_settings[ctx.guild]

        if len(args) == 0:
            await ctx.send(embed=await sett.format())
            return

        args_list = list(args)
        args_list.remove(args[0])

        response = await sett.write(args[0], " ".join(args_list), ctx)

        if response is None:
            await ctx.send("`Error: Setting not found`")
        elif response is True:
            await ctx.send("Setting updated!")

    @app_commands.command(name='addbot', description=config.HELP_ADDBOT, help=config.HELP_ADDBOT_SHORT)
    @commands.is_owner
    async def _addbot(self, ctx):
        embed = discord.Embed(title="Invite", description=config.ADD_MESSAGE +
                              "(https://discordapp.com/oauth2/authorize?client_id={}&scope=bot>)".format(self.bot.user.id))

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
