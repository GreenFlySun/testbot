import discord
from discord.ext import commands
import random

class random_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="rm", help="случайно выдаёт 1 число\слово")
    async def random(self,ctx,*items):
        await ctx.send("Пожалуй я выберу  " + random.choice(items))

    @commands.command(name="rd", help="random dice.Случайное число от 0 до вашего введённого")
    async def dice(self,ctx,item):
        try:
            num = random.randint(0, int(item))
            await ctx.send("Хочу выбрать это число ")
            await ctx.send(num)
        except:
            await ctx.send("Не-не-не,давай числа,а не слова,Slave")