import discord, logging
from discord import ui, app_commands
from musicbot import utils
from musicbot.speed_logger import profile


@app_commands.context_menu(name="play")
@app_commands.guild_only
async def _context_play(inter:discord.Interaction, message:discord.Message):
    if not inter.response.is_done(): await inter.response.defer()
    await inter.client.get_cog('Music')._play_song.callback(inter.client.get_cog('Music'), inter, track=message.content)

class music_buttons(ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)


    #prev button
    @ui.button(label="Prev")
    async def _prev(self, inter:discord.Interaction, button:ui.Button):
        await inter.response.defer()
        await inter.client.get_cog('Music')._prev.callback(self=inter.client.get_cog('Music'), ctx=inter)


    #play/pause button
    @ui.button(label="Pause", style=discord.ButtonStyle.green)
    async def _play_pause(self, inter:discord.Interaction, button:ui.Button):
        await inter.response.defer()
        current_guild = inter.guild

        if (not current_guild.voice_client or not current_guild.voice_client.is_paused()) and not current_guild.voice_client.is_playing():
            message = inter.message.reference
            logging.info(message)


        if await utils.play_check(inter) == False:
            return
        if current_guild.voice_client.is_playing():
            button.label = "Paused"
            button.style = discord.ButtonStyle.red
            await self.bot.get_cog('Music')._pause.callback(self=inter.client.get_cog('Music'), ctx=inter)
        else:
            button.label = "Pause"
            button.style = discord.ButtonStyle.green
            await self.bot.get_cog('Music')._resume.callback(self=inter.client.get_cog('Music'), ctx=inter)
        await inter.message.edit(view=self)
    

    #next button
    @ui.button(label="Next")
    async def _skip(self, inter:discord.Interaction, button:ui.Button):
        await inter.response.defer()
        await self.bot.get_cog('Music')._skip.callback(self=inter.client.get_cog('Music'), ctx=inter)