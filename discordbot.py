import discord
from discord.ext import commands
import dotenv
import os 
import wavelink
import logging


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

dotenv.load_dotenv()

token = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.members=True
intents.message_content=True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.lower()=="merhaba":
        await message.channel.send("merhaba")
    await bot.process_commands(message)

@bot.event
async def on_member_join(ctx):
    channel_id=1440453854385803416
    channel = ctx.guild.get_channel(channel_id)
    embed = discord.Embed(title="Kim Gelmiiş😮",description=f"Sunucudan alabildiğin kadar zevk al {ctx.mention}")
    embed.add_field(name=f"Sunucuya hoşgeldin!",value="#chat de istediğin kadar konuşabilir. Ses kanallarında bir o kadar sohbetlere dahil olup sıkıntını giderebilirsin.")
    embed.set_author(name="MC Studio")
    embed.set_image(url="https://ares.shiftdelete.net/2021/08/arkadaslarinizla-izleyebileceginiz-en-iyi-komedi-filmleri-deadpool.jpg")
    await channel.send(embed=embed )

@bot.command(guild_ids=["1221034983225954344"])
async def gtn(ctx):
    """A Slash Command to play a Guess-the-Number game."""

    await ctx.respond('Guess a number between 1 and 10.')
    while True:
        guess = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if int(guess.content) == 5:
            await ctx.send('You guessed it!')
            break
        else:
            await ctx.send('Nope, try again.')

@bot.command(guild_ids=["1221034983225954344"])
async def poll(ctx,*,questions,title):
    embed = discord.Embed(title=title, description=questions)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command(guild_ids=["1221034983225954344"])
async def hello(member):
    await member.respond("hello")


bot.run(token)