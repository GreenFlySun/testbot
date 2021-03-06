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

    @commands.command(name="p", help="?????????????????? ?????????? ?? ??????????")
    async def p(self, ctx, *args):
        query = ""
        query += " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:

            await ctx.send("?? ???? ???????? ???????? ?????? ????????????????,?????????? ?????? ???????? ????????! <:12:762323100267839528>")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("???? ???????? ?????????????????? ??????????,Letherman. ?? ?????? ?????? ???? ???? ?????? <:10:762324522794745867>")
            else:
                await ctx.send("?????????? ?? ??????????????,Letherman <:1_:762324484929617961>")
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="q", help="???????????????????? ??????????????")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += str(i+1)+". " + self.music_queue[i][0]['title'] + "\n"
            print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("???????? ???????? ?? ????????????,Slave <:10:762322853206294548>")

    @commands.command(name="skip", help="???????????????????? ??????????")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await ctx.send("???????? ????????????,???????????????????? ???????? <:2_:762324496191193095>")
            await self.play_music()
        else:
            await ctx.send("???????????? ????????????????????,?????? <:__:762321616130015232>")

    @commands.command(name="clear", help ="???????????? ??????????????")
    async def clear(self,ctx):
        self.music_queue.clear()
        await ctx.send("?????????????????? ???? ?????? ??????????????,Slaves")

    @commands.command(name="del", help= "?????????????? ???????????????????????? ???? ??????????????")
    async def del_from_queue(self,ctx,item):
        await ctx.send("?? ?????????? ???? ?????????????? ???????? ????????,Slave - " + self.music_queue[int(item) - 1][0]['title'])
        self.music_queue.pop(int(item) - 1)


    @commands.command(name="pause", help="??????????")
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
            await ctx.send("???????? ???????? ???? ??????????,Boy <:12:762323100267839528>")

    @commands.command(name="resume", help="???????????????????? ?????????????????????? ????????")
    async def resume(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.resume()
            await ctx.send("?????? ?????? ??????????")

    @commands.command(name="np", help="?????? ???????????? ????????????")
    async def now_play(self, ctx):
        if self.vc != "" and self.vc:
            await ctx.send("???????????? ?????????????????? - "+ str(self.np) + "<:11:762324532064550923>")
        else:
            await ctx.send("???????????? ???? ????????????,Letherman <:1_:762324484929617961>")

    @commands.command(name="fs", help="???????????????????????? ???? ???????????? ???????????? ??????????????")
    async def fs(self, ctx,*num):
        k = 0
        for i in num:
            await ctx.send("?? ?????????????????? ???????? ???????? ???????? ???????????? -" + self.music_queue[int(i) - 1][0]['title'])
        for i in num[::-1]:
            self.music_queue.insert(0, (self.music_queue[int(i)-1+k]))
            k = k + 1
        num = sorted(num)
        for i in num[::-1]:
            self.music_queue.pop(int(i)+len(num) - 1)


    @commands.command(name="dc", help="???????????? ?? ????????????")
    async def dc(self, ctx):
        await ctx.send("??????????,College Boy <:10:762322853206294548>")
        await self.vc.disconnect()

    @commands.command(name="test", help= "Test")
    async def test(self,ctx):
        await ctx.send(self.music_queue[0])
