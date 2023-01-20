import asyncio

import discord
from config import config
from discord.ext import commands
from discord import app_commands
from musicbot import linkutils, utils


class Music(commands.Cog):
    """ A collection of the commands related to music playback.

        Attributes:
            bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='play', description=config.DESCRIPTION_YT)
    async def _play_song(self, ctx:discord.Interaction, *, track: str):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if (await utils.is_connected(ctx) == None):
            if await audiocontroller.uconnect(ctx) == False:
                return

        if track.isspace() or not track:
            return

        if await utils.play_check(ctx) == False:
            return

        # reset timer
        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if audiocontroller.playlist.loop == True:
            await ctx.send("Loop is enabled! Use {}loop to disable".format(config.BOT_PREFIX))
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:

            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING))
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)

    @app_commands.command(name='loop', description=config.DESCRIPTION_LOOP)
    async def _loop(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            await ctx.send("No songs in queue!")
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            await ctx.send("Loop enabled :arrows_counterclockwise:")
        else:
            audiocontroller.playlist.loop = False
            await ctx.send("Loop disabled :x:")

    @app_commands.command(name='shuffle', description=config.DESCRIPTION_SHUFFLE)
    async def _shuffle(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        audiocontroller.playlist.shuffle()
        await ctx.send("Shuffled queue :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @app_commands.command(name='pause', description=config.DESCRIPTION_PAUSE)
    async def _pause(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.send("Playback Paused :pause_button:")

    @app_commands.command(name='queue', description=config.DESCRIPTION_QUEUE)
    async def _queue(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send("Queue is empty :x:")
            return

        playlist = utils.guild_to_audiocontroller[current_guild].playlist

        # Embeds are limited to 25 fields
        if config.MAX_SONG_PRELOAD > 25:
            config.MAX_SONG_PRELOAD = 25

        embed = discord.Embed(title=":scroll: Queue [{}]".format(
            len(playlist.playque)), color=config.EMBED_COLOR, inline=False)

        for counter, song in enumerate(list(playlist.playque)[:config.MAX_SONG_PRELOAD], start=1):
            if song.info.title is None:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.webpage_url, song.info.webpage_url), inline=False)
            else:
                embed.add_field(name="{}.".format(str(counter)), value="[{}]({})".format(
                    song.info.title, song.info.webpage_url), inline=False)

        await ctx.send(embed=embed)

    @app_commands.command(name='stop', description=config.DESCRIPTION_STOP)
    async def _stop(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.send("Stopped all sessions :octagonal_sign:")

    @app_commands.command(name='move', description=config.DESCRIPTION_MOVE)
    async def _move(self, ctx, oldindex:int, newindex:int):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Queue is empty :x:")
            return
        try:
            audiocontroller.playlist.move(oldindex - 1, newindex - 1)
        except IndexError:
            await ctx.send("Wrong position")
            return
        await ctx.send("Moved")

    @app_commands.command(name='skip', description=config.DESCRIPTION_SKIP)
    async def _skip(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Queue is empty :x:")
            return
        current_guild.voice_client.stop()
        await ctx.send("Skipped current song :fast_forward:")

    @app_commands.command(name='clear', description=config.DESCRIPTION_CLEAR)
    async def _clear(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.send("Cleared queue :no_entry_sign:")

    @app_commands.command(name='prev', description=config.DESCRIPTION_PREV)
    async def _prev(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await ctx.send("Playing previous song :track_previous:")

    @app_commands.command(name='resume', description=config.DESCRIPTION_RESUME)
    async def _resume(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()
        await ctx.send("Resumed playback :arrow_forward:")

    @app_commands.command(name='songinfo', description=config.DESCRIPTION_SONGINFO)
    async def _songinfo(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output(config.SONGINFO_SONGINFO))

    @app_commands.command(name='history', description=config.DESCRIPTION_HISTORY)
    async def _history(self, ctx):
        await ctx.response.defer()

        current_guild = utils.get_guild(self.bot, ctx)

        if await utils.play_check(ctx) == False:
            return

        if current_guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return
        await ctx.send(utils.guild_to_audiocontroller[current_guild].track_history())

    @app_commands.command(name='volume', description=config.DESCRIPTION_VOL)
    async def _volume(self, ctx, volume: int = None):
        await ctx.response.defer()

        if ctx.guild is None:
            await ctx.send(config.NO_GUILD_MESSAGE)
            return

        if await utils.play_check(ctx) == False:
            return

        if not volume:
            await ctx.send("Current volume: {}% :speaker:".format(utils.guild_to_audiocontroller[ctx.guild]._volume))
            return

        try:
            if volume > 100 or volume < 0:
                raise Exception('')
            current_guild = utils.get_guild(self.bot, ctx)

            if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
                await ctx.send('Volume set to {}% :sound:'.format(str(volume)))
            else:
                await ctx.send('Volume set to {}% :loud_sound:'.format(str(volume)))
            utils.guild_to_audiocontroller[current_guild].volume = volume
        except:
            await ctx.send("Error: Volume must be a number 1-100")


async def setup(bot):
    await bot.add_cog(Music(bot))
