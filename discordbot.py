import discord
from discord.ext import commands
import lavalink
from discord import Embed, utils
import dotenv
import os 
import logging

# 1. Loglama Ayarları
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# 2. Token Yükleme
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# 3. Bot Ayarları
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ---------------------------------------------------------
# MUSIC COG (Müzik Sistemi Sınıfı)
# ---------------------------------------------------------
class MusicCog(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        # Bot hazır olduğunda Lavalink'i başlatacağız
        if not hasattr(bot, 'music'): 
            self.bot.music = lavalink.Client(self.bot.user.id)
            # Lavalink Bağlantısı (IPv4 Zorlaması: 127.0.0.1)
            self.bot.music.add_node(
                host="127.0.0.1", 
                port=2333, 
                password="youshallnotpass", 
                region="eu", 
                name="music-node"
            )
            self.bot.add_listener(self.bot.music.voice_update_handler, "on_socket_response")
            self.bot.music.add_event_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    # KOMUT: /join
    @discord.slash_command(name="join", description="Ses kanalına katılır",guild_ids=[1221034983225954344])
    async def join(self, ctx):
        member = ctx.author
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id)
            
            if not player.is_connected:
                player.store("channel", ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))
            
            await ctx.respond(f"✅ **{vc.name}** kanalına bağlandım!")
        else:
            await ctx.respond("❌ Önce bir ses kanalına katılmalısın.")

    # KOMUT: /play
    @discord.slash_command(name="play", description="Müzik çalar", guild_ids=[1221034983225954344])
    async def play(self, ctx, query: str):
        # İşlem uzun sürebilir diye defer atıyoruz
        await ctx.defer()
        
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            # Eğer bot seste değilse otomatik bağlanmayı dene
            if not player.is_connected:
                if ctx.author.voice:
                    await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
                else:
                    return await ctx.respond("❌ Bir ses kanalında değilsin.")

            query = f"ytsearch:{query}"
            results = await player.node.get_tracks(query)
            
            if not results or not results['tracks']:
                return await ctx.respond("Sonuç bulunamadı.")

            tracks = results["tracks"][0:10]
            i = 0
            query_result = ""
            for track in tracks:
                i = i + 1 
                query_result = query_result + f"{i}) {track['info']['title']} - {track['info']['uri']}\n"
            
            embed = Embed(description=query_result)
            await ctx.respond(embed=embed)
            
            def check(m):
                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
            
            try:
                response = await self.bot.wait_for("message", check=check, timeout=30.0)
            except:
                return await ctx.followup.send("Süre doldu, seçim yapmadın.")

            # Sayı seçimi hatası düzeltildi
            selection = int(response.content) - 1
            if 0 <= selection < len(tracks):
                track = tracks[selection]
                player.add(requester=ctx.author.id, track=track)
                
                await ctx.followup.send(f"🎵 Listeye eklendi: **{track['info']['title']}**")
                
                if not player.is_playing:
                    await player.play()
            else:
                await ctx.followup.send("Geçersiz numara.")

        except Exception as error:
            print(f"Hata: {error}")
            await ctx.followup.send("Bir hata oluştu.")

# ---------------------------------------------------------
# BOT EVENTLERİ
# ---------------------------------------------------------

@bot.event
async def on_ready():
    print(f"✅ Giriş yapıldı: {bot.user.name}")
    
    # Music Cog'unu burada yüklüyoruz
    bot.add_cog(MusicCog(bot))
    print("🎹 Müzik sistemi yüklendi.")

    # Komutları senkronize et (Bu işlem biraz zaman alabilir ama garanti olur)
    # Global senkronizasyon için:
    # await bot.sync_commands() 
    print("Komutlar hazir!")

@bot.event
async def on_member_join(member):
    channel_id = 1440453854385803416
    channel = member.guild.get_channel(channel_id)
    if channel:
        embed = discord.Embed(title="Kim Gelmiiş😮", description=f"Sunucudan alabildiğin kadar zevk al {member.mention}")
        embed.add_field(name="Sunucuya hoşgeldin!", value="#chat de istediğin kadar konuşabilir...")
        embed.set_author(name="MC Studio")
        embed.set_image(url="https://ares.shiftdelete.net/2021/08/arkadaslarinizla-izleyebileceginiz-en-iyi-komedi-filmleri-deadpool.jpg")
        await channel.send(embed=embed)

# Diğer komutlar (gtn, poll, hello)

@bot.command()
async def gtn(ctx):
    await ctx.send('Guess a number between 1 and 10.')
    # ... oyun mantığı ...

@bot.slash_command(name="hello", description="Selam verir",guild_ids=[1221034983225954344])
async def hello(ctx):
    await ctx.respond("hello")

# Botu çalıştır
if __name__ == "__main__":
    bot.run(token)