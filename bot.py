import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from itertools import cycle
from urllib.parse import urlparse
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
import asyncio
import chalk
import random
import youtube_dl
import traceback
import sys
import time
import shlex
import os
import re
import io
import datetime
import requests
from googletrans import Translator
from PIL import Image, ImageDraw
from pyfiglet import figlet_format, FontNotFound


bot = commands.Bot(command_prefix='*')
bot.remove_command('help')
initial_extensions = ['Music', 'Google', 'CommandErrorHandler']
rr_bullet = random.randint(1, 6)
rr_count = 1
translator = Translator(service_urls=[
	'translate.google.com',
	'translate.google.co.kr',
])

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

LANGCODES = dict(map(reversed, LANGUAGES.items()))

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()
#BotEvent
@bot.event
async def on_ready():
    print  ('Evix Online')
    print ("Discord.py " + discord.__version__)
    await bot.change_presence(activity=discord.Game(name="*help"))

#BotCommand
@bot.command(aliases=["Test"])
async def test(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		await ctx.send(f"Test Done, Bot Working {ctx.author.mention}!")

@bot.command()
async def translate(ctx, lang,*, message:str):
    if not ctx.guild:
        await ctx.send('This command can not be used in Private Messages.')
    else:
        emb_5 = discord.Embed(title="Translator")
        emb_5.add_field(name="Message Given", value=message)
        emb_5.add_field(name="Detected Language", value=translator.detect(message).lang)
        translated = translator.translate(text=message, dest=lang, src='auto')
        emb_5.add_field(name="Translation Language", value=lang)
        emb_5.add_field(name="Translated Message ", value=translated.text, inline=True)
        emb_5.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Google_Translate_logo.svg/1200px-Google_Translate_logo.svg.png")
        emb_5.set_footer(text="Special thanks to astolfo is my waifu#6847")
        await ctx.send(embed=emb_5)

@bot.command()
async def shutdown(ctx):
	member = discord.Member
	if ctx.author.id == 429933485868711937:
		await bot.logout()
	else:
		await ctx.send("❌❌ Error! Only the developer can shutdown the bot❌❌")
		print(f"The user {ctx.message.author} in the server {ctx.guild.name} tried to shutdown the bot")

@bot.command(invoke_without_command=True)
async def ascii(ctx, text: str, font: str, textcolor: str = '', background: str = ''):
    if not ctx.guild:
        await ctx.send('This command can not be used in Private Messages.')
    else:
        if not textcolor:
            textcolor = "white"
        if not background:
            background = "black"
        if font == "barbwire":
            text = text.replace("", " ")
        img = Image.new('RGB', (2000, 1000))
        d = ImageDraw.Draw(img)
        try:
            d.text((20, 20), figlet_format(text, font=font), fill=(255, 0, 0))
            text_width, text_height = d.textsize(figlet_format(text, font=font))
            img1 = Image.new('RGB', (text_width + 30, text_height + 30), background)
            d = ImageDraw.Draw(img1)
            d.text((20, 20), figlet_format(text, font=font), fill=textcolor, anchor="center")
            temp = io.BytesIO()
            img1.save(temp, format="png")
            temp.seek(0)
            await ctx.send(file=discord.File(filename="ascii.png", fp=temp))
        except FontNotFound:
            await ctx.send(f"`{font}` seems to not be a valid font. Try looking here: "
                           "http://www.figlet.org/examples.html")

@bot.command()
async def russianroulette(ctx):
    if not ctx.guild:
        await ctx.send('This command can not be used in Private Messages.')
    else:
        await ctx.send('You spin the cylinder of the revolver with 1 bullet in it...')
        await asyncio.sleep(1)
        await ctx.send(':gun: ...you place the muzzle against your head and pull the trigger...')
        await asyncio.sleep(2)
        global rr_bullet, rr_count
        if rr_bullet == rr_count:
            await ctx.send(':dizzy_face: ...your brain gets splattered all over the wall.')
            rr_bullet = random.randint(1, 6)
            rr_count = 1
        else:
            await ctx.send(':grinning: ...you live to see another day.')
            rr_count += 1

@bot.command()
async def randomnumber(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		randomnum = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
		await ctx.send(random.choice(randomnum))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		await member.send(f'❌ You have been kicked from `{ctx.guild.name}` By {ctx.author.mention} Reason `{reason}`')
		await member.kick()
		await ctx.message.delete()
		embed = discord.Embed(title="❌ A user has been kicked from the server", description="All the informations below", color=0xd01818)
		embed.add_field(name="Nickname", value=member.name)
		embed.add_field(name="ID", value=member.id)
		embed.add_field(name="Status", value=member.status)
		embed.add_field(name="Role", value=member.top_role)
		embed.add_field(name="Kicked By", value=ctx.author.mention)
		embed.add_field(name="Reason", value=reason)
		embed.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def announce(ctx, *, announce=None):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		await ctx.message.delete()
		embed = discord.Embed(title="✅ An admin announced something important!", description="All the informations below", color=0xd01818)
		embed.add_field(name="Announced By", value=ctx.author.mention)
		embed.add_field(name="Announce", value=announce)
		embed.set_thumbnail(url=ctx.author.avatar_url)
		await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, arg1=None):
    if not ctx.guild:
        await ctx.send('This command can not be used in Private Messages.')
    else:
        if ctx.author.bot:
            print('bot tried to send message and was denied')
        else:
            embed = discord.Embed(title="✅ Someone started a poll!", description="All the informations below", color=0xd01818)
            embed.add_field(name="Started By", value=ctx.author.mention, inline=True)
            embed.add_field(name="Poll", value=arg1, inline=True)
            embed.add_field(name="Answer👍", value="Yes!", inline=False)
            embed.add_field(name="Answer👎", value="No!", inline=False)
            embed.add_field(name="Answer🤷", value="I Don't Know!", inline=False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.message.delete()
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await msg.add_reaction('🤷')
		
@bot.command()
@commands.has_permissions(kick_members=True)
async def info(ctx, member: discord.Member):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		embed = discord.Embed(title="✅ Info About The User", description="All the informations below", color=0xd01818)
		embed.add_field(name="Nickname", value=member.name)
		embed.add_field(name="ID", value=member.id)
		embed.add_field(name="Status", value=member.status)
		embed.add_field(name="Roles", value=member.top_role)
		embed.add_field(name="Joined The Server", value=member.joined_at)
		embed.add_field(name="Info Requested By", value=ctx.author.mention)
		embed.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed=embed)
		await ctx.message.delete()

@bot.command()
async def botinfo(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		embed = discord.Embed(title="Created By", description="<@429933485868711937>", color=0xd01818)
		embed.add_field(name="Special Thanks To", value="<@241934089635102722> and <@361996747687591936>", inline=True)
		embed.set_footer(text="Discord.py")
		embed.set_author(name="Evix The Wizard")
		embed.add_field(name="Creation Date", value="11/08/2018", inline=False)
		embed.add_field(name="Help & Contacts", value="[Click Here](https://discord.gg/9geJMm3)", inline=True)
		embed.add_field(name="Invite Me!", value="[Click Here](https://bit.ly/2MF8Ost)", inline=False)
		await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		embed = discord.Embed(title="✅ Info About The Server", description="All the informations below", color=0xd01818)
		embed.add_field(name="Name", value=ctx.message.guild.name, inline=True)
		embed.add_field(name="ID", value=ctx.message.guild.id, inline=True)
		embed.add_field(name="Roles", value=len(ctx.message.guild.roles), inline=True)
		embed.add_field(name="Members", value=len(ctx.message.guild.members))
		embed.set_thumbnail(url=ctx.message.guild.icon_url)
		embed.add_field(name="Owner", value=ctx.guild.owner.mention)
		embed.add_field(name="Info Requested By", value=ctx.author.mention)
		await ctx.send(embed=embed)
		await ctx.message.delete()

@bot.command()
async def ip(ctx, ip=None):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		await ctx.send("https://check-host.net/ip-info?host=" + ip)

@bot.command()
async def ask(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		ask = ["The Wizard Says Yes","The Wizard Says No","The Wizard Says Probably","The Wizard Says Maybe","The Wizard Says Obviously Yes","The Wizard Says Obviously Not","The Wizard can't figure it out right now"]
		embed = discord.Embed(title=random.choice(ask), description="", color=0xd01818)
		await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
	if not ctx.guild:
		await ctx.send('This command can not be used in Private Messages.')
	else:
		user = ctx.message.author
		embed = discord.Embed(title="👋Hi!", description="Here are all the commands!", color=0xd01818)
		em = discord.Embed(title=":mailbox_with_mail: I sent you a dm", description="", color=0xd01818)
		embed.add_field(name="💣Admin", value="`Onlye admins can do this!`", inline=False)
		embed.add_field(name="*kick @user [reason]", value="Kick a user from the server, remember to add a reason!", inline=False)
		embed.add_field(name="*info @user", value="Show all the user's info", inline=False)
		embed.add_field(name="*announce [description] ", value="Make An announce to the server", inline=False)
		embed.add_field(name="💡Utilities", value="`Some utilities you can use!`", inline=False)
		embed.add_field(name="*randomnumber", value="Gives you a random number between 1 and 10", inline=False)
		embed.add_field(name="*botinfo", value="Show the bot's developer", inline=False)
		embed.add_field(name="*serverinfo", value="Gives you all the informations about the server", inline=False)
		embed.add_field(name="*ip [host]", value="Get an ip's informations", inline=False)
		embed.add_field(name="*poll [description]", value="Create a poll, between '' '' put your question", inline=False)
		embed.add_field(name=":joy: Funny", value="`Let's laugh togheter!`", inline=False)
		embed.add_field(name="*ask [text]", value="Ask a question to the bot", inline=False)
		embed.add_field(name="*russianroulette", value="Play russian roulette", inline=False)
		embed.add_field(name=":musical_note: Musical", value="`It's Musice timeeee`", inline=False)
		embed.add_field(name="*join", value="Make the bot join your channel", inline=False)
		embed.add_field(name="*play [url]", value="Play music from youtube, remember to add an url", inline=False)
		embed.add_field(name="*volume [value]", value="Change the song's volume", inline=False)
		embed.add_field(name="*queue", value="Shows you the queue", inline=False)
		embed.add_field(name="*skip", value="Skip the current song", inline=False)
		embed.add_field(name="*pause", value="Pause the current song", inline=False)
		embed.add_field(name="*resume", value="Resume the stopped music", inline=False)
		embed.add_field(name="*playing", value="Shows you which song is playing", inline=False)
		embed.add_field(name=":earth_asia: Google", value="`Google Commands`", inline=False)
		embed.add_field(name="*translate [language] [Text] ", value="Translate everything in every language, just with a command", inline=False)
		embed.add_field(name="*search [Text] ", value="Search Everything on google", inline=False)
		embed.set_footer(text="Discord.py")
		embed.set_author(name="Evix The Wizard")
		await user.send(embed=embed)
		await ctx.send(embed=em)

bot.run("YOUR TOKEN")
