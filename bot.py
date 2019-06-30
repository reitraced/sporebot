import discord
from discord.ext import commands
from SporeAPICoreUtils import *

p = '--'
client = commands.Bot(command_prefix=p)

f = open('token.txt', 'r')
token = f.read()
f.seek(0)
f.close()

f = open('game.txt', 'r')
lastgame = f.read()
f.seek(0)
f.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=lastgame))

@client.command(pass_context=True, brief="Print info about bot")
async def about(ctx):
    f = open('about.txt', 'r')
    await ctx.send(f.read())
    f.seek(0)
    f.close()

@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 4)*1000) + ' ms')


@client.command(brief="displays profile information about user")
async def profile(ctx, *, arg):
    GetProfileForUser(arg)
    url = ProfileForUserURL(arg)
    myxml = GetXMLForREST(url)
    if(myxml):
        tagline = str(TryGetNodeValues(myxml, "tagline"))
        
    file = discord.File("Downloads/" + arg + ".jpg", filename=arg + ".jpg")
    embed = discord.Embed(
        title=arg,
        description=tagline
    )
    embed.set_image(url="attachment://" + arg + ".jpg")
    await ctx.send(file=file, embed=embed)

client.run(token)