import discord
from discord import app_commands
from discord.ext import commands
from musicbot.commands import music
from musicbot import utils, songinfo
from config import config

stations = {
    "Radio Brony":"https://radiobrony.live/hls/aac_hifi.m3u8",
    "Brony Radio Germany":"http://radio.bronyradiogermany.com:8000/opus",
    "The Rock":"https://icecast.mediaworks.nz/rock_128kbps",
    "More FM":"https://livestream.mediaworks.nz/radio_origin/more_[CHC]_128kbps/playlist.m3u8",
    "The Edge":"https://livestream.mediaworks.nz/radio_origin/edge_[QTN]_128kbps/chunklist.m3u8",
    "George FM":"https://livestream.mediaworks.nz/radio_origin/george_[QTN]_128kbps/playlist.m3u8",
    "Hauraki":"https://ais-nzme.streamguys1.com/nz_009/playlist.m3u8?aw_0_1st.playerid=iHeartRadioWebPlayer&aw_0_1st.skey=6067669815&clientType=web&companionAds=false&deviceName=web-desktop&dist=iheart&host=webapp.NZ&listenerId=&playedFrom=157&pname=live_profile&profileId=6067669815&stationid=6191&terminalId=162&territory=NZ",
    "The Hits":"https://ais-nzme.streamguys1.com/nz_006/playlist.m3u8?aw_0_1st.playerid=iHeartRadioWebPlayer&aw_0_1st.skey=6067669815&clientType=web&companionAds=false&deviceName=web-desktop&dist=iheart&host=webapp.NZ&listenerId=&playedFrom=157&pname=live_profile&profileId=6067669815&stationid=6199&terminalId=162&territory=NZ"
    }

class Extra(commands.Cog):
    """ A collection of extra commands for the bot in your server.

            Attributes:
                bot: The instance of the bot that is executing the commands.
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    #sync commands with discord
    @app_commands.command(name="sync")
    @commands.is_owner
    async def _sync(self, inter:discord.Interaction) -> None:
        self.bot.tree.sync()

    
    #play radio stream
    @app_commands.command(name="radio", description="Plays the radio")
    @app_commands.guild_only
    @app_commands.choices(station=[app_commands.Choice(name=station, value=station) for station in stations.keys()])
    async def _radio(self, inter:discord.Interaction, station:str) -> None:
        
        await utils.guild_to_audiocontroller[inter.guild].stop_player()
        await self.bot.get_cog('Music')._play_song.callback(self, inter, track=stations[station])
        song = songinfo.Song.Sinfo("Internet",station,-1,None,None)
        await inter.send(embed=song.format_output("Now Playing"))
    
    #autocompleate radio stream command
    @_radio.autocomplete("station")
    async def _radio_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        return [app_commands.Choice(name=station, value=station) for station in stations.keys() if current.lower() in station.lower()]



async def setup(bot) -> None:
    await bot.add_cog(Extra(bot))