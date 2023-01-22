import discord

async def send(inter:discord.Interaction,content=None,*args,**kwargs):
        #if content:
        #    content = f"```{content}```"
        if inter.response.is_done(): message = await inter.edit_original_response(content=content,*args,**kwargs)
        else: message = await inter.response.send_message(content=content,*args,**kwargs)
        return message
setattr(discord.Interaction,"send",send)