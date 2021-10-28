import discord
from discord.ext import commands
from music_cog import music_cog
bot = commands.Bot(command_prefix='!')
bot.add_cog(music_cog(bot))

bot.run('OTAyNTEwODUwNzMxMDQ5MDIx.YXfeug.zDxMrOI11ZRSNPQ1213hcXl_4Zc')