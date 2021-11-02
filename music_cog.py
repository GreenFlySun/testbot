import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        self.is_playing = False


        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': False, 'default_search': 'auto'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.np = ""
        self.vc = ""


    def search_yt(self, item):
        if item[:5] == "https":
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(item, download=False)['entries'][0]
                except Exception:
                    return False
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(f'ytsearch:%s' % item, download=False)['entries'][0]
                except Exception:
                    return False

        return {'source':info['formats'][0]['url'], 'title': info['title']}


    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.np = ""
            self.np +=self.music_queue[0][0]['title']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
                self.np = ""
                self.np += self.music_queue[0][0]['title']
                self.music_queue.pop(0)
            else:
                await self.vc.move_to(self.music_queue[0][1])


            print(self.music_queue)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="p", help="запускает песню в Ютуба")
    async def p(self, ctx, *args):
        query = ""
        query += " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:

            await ctx.send("Я не знаю куда мне заходить,зайди сам куда либо! <:12:762323100267839528>")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Не могу проиграть песню,Letherman. С ней что то не так <:10:762324522794745867>")
            else:
                await ctx.send("Песня в очереди,Letherman <:1_:762324484929617961>")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="q", help="Показывает очередь")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += str(i+1)+". " + self.music_queue[i][0]['title'] + "\n"
            print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Нету гачи в списке,Slave <:10:762322853206294548>")

    @commands.command(name="skip", help="пропускает песню")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await ctx.send("идём дальше,пропускаем трек <:2_:762324496191193095>")
            await self.play_music()
        else:
            await ctx.send("Нечего пропускать,алё <:__:762321616130015232>")

    @commands.command(name="clear", help ="Чистит очередь")
    async def clear(self,ctx):
        self.music_queue.clear()
        await ctx.send("Почистили за вас очередь,Slaves")

    @commands.command(name="del", help= "Удаляет определенное из очереди")
    async def del_from_queue(self,ctx,item):
        await ctx.send("Я убрал из очереди этот трек,Slave - " + self.music_queue[int(item) - 1][0]['title'])
        self.music_queue.pop(int(item) - 1)


    @commands.command(name="pause", help="пауза")
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
            await ctx.send("Этот трек на паузе,Boy <:12:762323100267839528>")

    @commands.command(name="resume", help="продолжает производить трек")
    async def resume(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.resume()
            await ctx.send("Щас всё будет")

    @commands.command(name="np", help="Что сейчас играет")
    async def now_play(self, ctx):
        if self.vc != "" and self.vc:
            await ctx.send("Сейчас исполняет - "+ str(self.np) + "<:11:762324532064550923>")
        else:
            await ctx.send("Ничего не играет,Letherman <:1_:762324484929617961>")

    @commands.command(name="fs", help="перекидывает на начало списка очереди")
    async def fs(self, ctx,*num):
        k = 0
        for i in num:
            await ctx.send("Я передвину этот гачи трек повыше -" + self.music_queue[int(i) - 1][0]['title'])
        for i in num[::-1]:
            self.music_queue.insert(0, (self.music_queue[int(i)-1+k]))
            k = k + 1
        num = sorted(num)
        for i in num[::-1]:
            self.music_queue.pop(int(i)+len(num) - 1)


    @commands.command(name="dc", help="ливает с канала")
    async def dc(self, ctx):
        await ctx.send("Удачи,College Boy <:10:762322853206294548>")
        await self.vc.disconnect()

    @commands.command(name="test", help= "Test")
    async def test(self,ctx):
        await ctx.send(self.music_queue[0])
