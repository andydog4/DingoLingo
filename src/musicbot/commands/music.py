import asyncio, discord
from discord.ext import commands
from discord import app_commands
from config import config
from musicbot import linkutils, utils

from musicbot.plugins import button


class Music(commands.Cog):
    """ A collection of the commands related to music playback.

        Attributes:
            bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='play', description=config.DESCRIPTION_YT)
    @app_commands.guild_only
    async def _play_song(self, ctx:discord.Interaction, *, track: str) -> bool:
        if not ctx.response.is_done(): asyncio.create_task(ctx.response.defer())
        current_guild = ctx.guild
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
            await ctx.send("Loop is enabled! Use /loop to disable")
            return

        song = await audiocontroller.process_song(track)

        if song is None:
            await ctx.send(config.SONGINFO_ERROR)
            return

        if song.origin == linkutils.Origins.Default:
            
            view = button.music_buttons(bot=self.bot)
            if audiocontroller.current_song != None and len(audiocontroller.playlist.playque) == 0:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_NOW_PLAYING), view=view)
            else:
                await ctx.send(embed=song.info.format_output(config.SONGINFO_QUEUE_ADDED))

        elif song.origin == linkutils.Origins.Playlist:
            await ctx.send(config.SONGINFO_PLAYLIST_QUEUED)
        return True

    @app_commands.command(name='loop', description=config.DESCRIPTION_LOOP)
    @app_commands.guild_only
    async def _loop(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if len(audiocontroller.playlist.playque) < 1 and current_guild.voice_client.is_playing() == False:
            await ctx.send(config.QUEUE_EMPTY)
            return

        if audiocontroller.playlist.loop == False:
            audiocontroller.playlist.loop = True
            await ctx.send("Loop enabled :arrows_counterclockwise:")
        else:
            audiocontroller.playlist.loop = False
            await ctx.send("Loop disabled :x:")

    @app_commands.command(name='shuffle', description=config.DESCRIPTION_SHUFFLE)
    @app_commands.guild_only
    async def _shuffle(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if await utils.play_check(ctx) == False:
            return

        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send(config.QUEUE_EMPTY)
            return

        audiocontroller.playlist.shuffle()
        await ctx.send("Shuffled queue :twisted_rightwards_arrows:")

        for song in list(audiocontroller.playlist.playque)[:config.MAX_SONG_PRELOAD]:
            asyncio.ensure_future(audiocontroller.preload(song))

    @app_commands.command(name='pause', description=config.DESCRIPTION_PAUSE)
    @app_commands.guild_only
    async def _pause(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await ctx.send("Playback Paused :pause_button:")

    @app_commands.command(name='queue', description=config.DESCRIPTION_QUEUE)
    @app_commands.guild_only
    async def _queue(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            await ctx.send(config.QUEUE_EMPTY)
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
    @app_commands.guild_only
    async def _stop(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False
  
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await ctx.send("Stopped all sessions :octagonal_sign:")

    @app_commands.command(name='move', description=config.DESCRIPTION_MOVE)
    @app_commands.guild_only
    async def _move(self, ctx, oldindex:int, newindex:int):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send(config.QUEUE_EMPTY)
            return
        try:
            audiocontroller.playlist.move(oldindex - 1, newindex - 1)
        except IndexError:
            await ctx.send("Wrong position")
            return
        await ctx.send("Moved")

    @app_commands.command(name='skip', description=config.DESCRIPTION_SKIP)
    @app_commands.guild_only
    async def _skip(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send(config.QUEUE_EMPTY)
            return
        current_guild.voice_client.stop()
        await ctx.send("Skipped current song :fast_forward:")

    @app_commands.command(name='clear', description=config.DESCRIPTION_CLEAR)
    @app_commands.guild_only
    async def _clear(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.clear_queue()
        current_guild.voice_client.stop()
        audiocontroller.playlist.loop = False
        await ctx.send("Cleared queue :no_entry_sign:")

    @app_commands.command(name='prev', description=config.DESCRIPTION_PREV)
    @app_commands.guild_only
    async def _prev(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        audiocontroller.playlist.loop = False

        audiocontroller.timer.cancel()
        audiocontroller.timer = utils.Timer(audiocontroller.timeout_handler)

        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await ctx.send("Playing previous song :track_previous:")

    @app_commands.command(name='resume', description=config.DESCRIPTION_RESUME)
    @app_commands.guild_only
    async def _resume(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        current_guild.voice_client.resume()
        await ctx.send("Resumed playback :arrow_forward:")

    @app_commands.command(name='songinfo', description=config.DESCRIPTION_SONGINFO)
    @app_commands.guild_only
    async def _songinfo(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        song = utils.guild_to_audiocontroller[current_guild].current_song
        if song is None:
            return
        await ctx.send(embed=song.info.format_output(config.SONGINFO_SONGINFO))

    @app_commands.command(name='history', description=config.DESCRIPTION_HISTORY)
    @app_commands.guild_only
    async def _history(self, ctx):
        if not ctx.response.is_done(): await ctx.response.defer()

        current_guild = ctx.guild

        if await utils.play_check(ctx) == False:
            return

        await ctx.send(utils.guild_to_audiocontroller[current_guild].track_history())

    @app_commands.command(name='volume', description=config.DESCRIPTION_VOL)
    @app_commands.guild_only
    async def _volume(self, ctx, volume: int = None):
        if not ctx.response.is_done(): await ctx.response.defer()

        if await utils.play_check(ctx) == False:
            return

        if not volume:
            await ctx.send(f"Current volume: {utils.guild_to_audiocontroller[ctx.guild]._volume}% :speaker:", ephemeral=True)
            return

        if volume > 100 or volume < 0:
            await ctx.send("Error: Volume must be a number 1-100")
            return
 
        current_guild = ctx.guild

        if utils.guild_to_audiocontroller[current_guild]._volume >= volume:
            await ctx.send(f'Volume set to {volume}% :sound:')
        else:
            await ctx.send(f'Volume set to {volume}% :loud_sound:')
        utils.guild_to_audiocontroller[current_guild].volume = volume


async def setup(bot):
    await bot.add_cog(Music(bot))
