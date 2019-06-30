import discord
from discord.ext import commands
from SporeAPICoreUtils import *
import fnmatch
import os

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
async def profile(ctx, arg=None):
    if arg:
        buddies = str(len(GetBuddiesForUser(arg)))
        creations = str(len(GetAssetIdsForUser(arg)))
        profileurl = "https://www.spore.com/view/myspore/" + arg
#        try:
#            GetProfileForUser(arg)
#        except:
#            blankimage = "http://www.spore.com/static/war/images/global/avatar_none.png"
#            ext = blankimage[0].split(".")
#            FetchAndSave(blankimage[0], username + "." + ext[len(ext) - 1] )
        url = ProfileForUserURL(arg)
        myxml = GetXMLForREST(url)
        if(myxml):
            try:
                brackettagline = str(TryGetNodeValues(myxml, "tagline"))
                tagline = brackettagline[1:-1]
            except:
                tagline = " "
        
            try:
                listimage = TryGetNodeValues(myxml, "image")
                image = listimage[0]
            except:
                blankimage = "http://www.spore.com/static/war/images/global/avatar_none.png"
                image = blankimage
        else:
            tagline = "This account does not exist"
            buddies = "0"
            creations = "0"
            image = "http://www.spore.com/static/war/images/global/avatar_none.png"
        embed = discord.Embed(title=arg, url=profileurl)
        embed.add_field(name="Tagline", value=tagline)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Buddies", value="This player currently has " + buddies + " buddy(ies)")
        embed.add_field(name="Creations", value="This player has made " + creations + " creations")
        embed.set_footer(text="Thank you Maxis for this amazing API and game!")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Please provide a Spore screen name")

client.run(token)
