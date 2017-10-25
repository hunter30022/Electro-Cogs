# This cog is a modified version of Radio Haru by Mr. Boo Grande
import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import send_cmd_help
import asyncio

class RadioHaru:
    """Radio Haru - www.RadioHaru.pw"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True, no_pm=True)
    async def radioharu(self, ctx):
        """Radio Haru"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            await self.bot.say("https://radioharu.pw/")

    @radioharu.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def play(self, ctx):
        """Play Radio Haru"""
        server = ctx.message.server
        author = ctx.message.author
        if self.voice_connected(server):
            await self.bot.say("Already connected to a voice channel, use `{}radioharu stop` to change radio.".format(ctx.prefix))
        else:
            voice_channel = author.voice_channel
            voice = await self.bot.join_voice_channel(voice_channel)
            Channel = ctx.message.channel
            await self.bot.send_typing(Channel)
            player = voice.create_ffmpeg_player('https://cdn.discordapp.com/attachments/336598653923753987/360413654224601089/Radio-Haru.ogg')
            player.start()
            await asyncio.sleep(7)
            player.stop()
            player = voice.create_ffmpeg_player('https://stream.radioharu.pw/owo')
            player.start()
            await self.bot.say(":green_heart: **Playing Radio Haru!**")
            
    @radioharu.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def playwin(self, ctx):
        """Play Radio Haru - Use instead of play command if on a Windows machine."""
        server = ctx.message.server
        author = ctx.message.author
        if self.voice_connected(server):
            await self.bot.say("Already connected to a voice channel, use `{}radioharu stop` to change radio.".format(ctx.prefix))
        else:
            voice_channel = author.voice_channel
            voice = await self.bot.join_voice_channel(voice_channel)
            Channel = ctx.message.channel
            await self.bot.send_typing(Channel)
            player = voice.create_ffmpeg_player('https://cdn.discordapp.com/attachments/336598653923753987/360413654224601089/Radio-Haru.ogg')
            player.start()
            await asyncio.sleep(7)
            player.stop()
            await self._disconnect_voice_client(server)
            await self.bot.say(":green_heart: **Playing Radio Haru!**")
            radio = True
            while radio == True:
                voice = await self.bot.join_voice_channel(voice_channel)
                player = voice.create_ffmpeg_player('https://stream.radioharu.pw/owo')
                player.start()
                await asyncio.sleep(300)
                await self._disconnect_voice_client(server)

    @radioharu.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def stop(self, ctx):
        """Stop Radio Haru"""
        server = ctx.message.server
        author = ctx.message.author
        await self._disconnect_voice_client(server)
        voice_channel = author.voice_channel
        voice = await self.bot.join_voice_channel(voice_channel)
        player = voice.create_ffmpeg_player('https://cdn.discordapp.com/attachments/336598653923753987/360425539309142037/radioharu_goodbye.mp3')
        player.start()
        await asyncio.sleep(1)
        await self._disconnect_voice_client(server)
        await self.bot.say(":red_circle: **Stopped playing Radio!**")
        
    @radioharu.command(pass_context=True, no_pm=True)
    async def donate(self, ctx):
        """Donate for server costs"""
        await self.bot.say("**https://patreon.com/harukigrande/**")
        
    def voice_client(self, server):
        return self.bot.voice_client_in(server)

    def voice_connected(self, server):
        if self.bot.is_voice_connected(server):
            return True
        return False

    async def _disconnect_voice_client(self, server):
        if not self.voice_connected(server):
            return

        voice_client = self.voice_client(server)

        await voice_client.disconnect()

def setup(bot):
    bot.add_cog(RadioHaru(bot))
