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


@client.command()
async def github(ctx):
    await ctx.send("https://github.com/reitraced/sporebot")


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
async def profile(ctx, arg=None):
    if arg:
        buddies = str(len(GetBuddiesForUser(arg)))
        creations = str(len(GetAssetIdsForUser(arg)))
        profileurl = "https://www.spore.com/view/myspore/" + arg
        url = ProfileForUserURL(arg)
        myxml = GetXMLForREST(url)

        if(myxml):
            try:
                brackettagline = str(TryGetNodeValues(myxml, "tagline"))
                tagline = brackettagline[1:-1]
            except:
                tagline = " "

            if not TryGetNodeValues(myxml, "image") == ['http://www.spore.com/static/null']:
                try:
                    listimage = TryGetNodeValues(myxml, "image")
                    image = listimage[0]
                except:
                    blankimage = "http://www.spore.com/static/war/images/global/avatar_none.png"
                    image = blankimage

            else:
                blankimage = "http://www.spore.com/static/war/images/global/avatar_none.png"
                image = blankimage
                tagline = "Player not found"
                buddies = "0"
                creations = "0"

        embed = discord.Embed(title=arg, description=tagline, url=profileurl)
        embed.set_thumbnail(url=image)
        embed.add_field(
            name="Buddies", value="This player currently has " + buddies + " buddy(ies)")
        embed.add_field(
            name="Creations", value="This player has made " + creations + " creations")
        embed.set_footer(text="Thank you Maxis for this amazing API and game!")

        await ctx.send(embed=embed)

    else:
        await ctx.send("Please provide a Spore screen name")

@client.command()
async def info(ctx, arg=None):
    if arg:
        desc = GetDescriptionForAsset(arg)[0]
        tags = str(GetTagsForAsset(arg))[1:-1]
        image = AssetURL(arg)
        assetinfo = InfoForAssetURL(arg)
        myxml = GetXMLForREST(assetinfo)
        if(myxml):
            try:
                name = TryGetNodeValues(myxml, "name")[0]
                author = TryGetNodeValues(myxml, "author")[0]
            except:
                name = "no name, wow congrats you glitched the system"

        embed = discord.Embed(title=name, description=desc)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Tags", value=tags)
        embed.add_field(name="Author", value=author)
        await ctx.send(embed=embed)
    
    if not arg:
        await ctx.send("Please provide a Spore Asset ID as an argument, to get an Asset ID please follow this guide: https://gist.github.com/reitraced/c7202576cc33fe4df12fb16888d3508d.")
            

@client.command()
async def stats(ctx):
    url = "http://www.spore.com/rest/stats"
    myxml = GetXMLForREST(url)
    num = []
    if(myxml):
        total = TryGetNodeValues(myxml, "totalUploads")[0]
        daily = TryGetNodeValues(myxml, "dayUploads")[0]
        await ctx.send("There are currently " + total + " creations on Spore, of which " + daily + " were made today!")
    else:
        await ctx.send("There was a problem connecting to Spore servers. Please try again later.")

@client.command()
async def users(ctx):
    url = "http://www.spore.com/rest/stats"
    myxml = GetXMLForREST(url)
    num = []
    if(myxml):
        total = TryGetNodeValues(myxml, "totalUsers")[0]
        daily = TryGetNodeValues(myxml, "dayUsers")[0]
        await ctx.send("There are currently " + total + " players registered on Spore, and " + daily + " registered today!")
    else:
        await ctx.send("There was a problem connecting to Spore servers. Please try again later.")

client.run(token)
