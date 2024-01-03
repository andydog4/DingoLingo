import os
from dotenv import load_dotenv
load_dotenv()

import discord, logging
from discord.ext import commands

from config import config
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings

import message_hook

initial_extensions = ['musicbot.commands.music', 'musicbot.commands.general',
                      "musicbot.commands.extra"]
config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

#new
class disClient(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    async def setup_hook(self) -> None:
        await super().setup_hook()

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                logging.error(e)


    async def on_ready(self) -> None:
        logging.info(config.STARTUP_MESSAGE)
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name="Music"))

        for guild in self.guilds:
            await self.register(guild)
            logging.info("Joined {}".format(guild.name))

        #await self.tree.sync() 
        logging.info(config.STARTUP_COMPLETE_MESSAGE)

        
    async def on_guild_join(self,guild) -> None:
        logging.info(guild.name)
        await self.register(guild)


    async def register(self,guild) -> None:

        guild_to_settings[guild] = Settings(guild)
        guild_to_audiocontroller[guild] = AudioController(self, guild)

        sett = guild_to_settings[guild]


        if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
            return

        vc_channels = guild.voice_channels

        if sett.get('vc_timeout') == False:
            if not sett.get('start_voice_channel') == None:
                for vc in vc_channels:
                    if vc.id == sett.get('start_voice_channel'):
                        try:
                            controler = guild_to_audiocontroller[guild]
                            await controler.register_voice_channel(vc_channels[vc_channels.index(vc)])
                            if not sett.get("autoplay_url") == "":
                                await controler.process_song(sett.get("autoplay_url"))
                                await controler.timer.cancel()
                        except Exception as e:
                            logging.error(e)


if __name__ == '__main__':

    if config.BOT_TOKEN == "":
        logging.error("Error: No bot token!")
        exit
    intents = discord.Intents.default()
    intents.message_content = True
    client = disClient(intents=intents, test_guilds=os.getenv("test_guilds"), command_prefix=config.BOT_PREFIX, case_insensitive=True)
    client.run(os.getenv("discord_bot_token"), reconnect=True, root_logger=True)