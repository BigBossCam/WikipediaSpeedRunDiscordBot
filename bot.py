import discord, wikipedia, random, os
from discord.ext import commands
from discord.utils import get

DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

# set prefix to '.'

bot = commands.Bot(command_prefix=".")

# make sure discord.py is initialized

@bot.event
async def on_ready():
    print("bot ready")

# Function to get a random article

def wikiRandom():
    getRandomArticle = wikipedia.random(pages=1)
    return getRandomArticle

# Get all links on an article

def wikiLinks(arg):
    getLinksonPage = wikipedia.page(arg)
    listOfLinksOnPage = getLinksonPage.links
    return listOfLinksOnPage

# Set global to make sure bot can only be used only once
# This is a hacky solution, trying to understand how async works

global checkIfRunning
checkIfRunning = False

# Usage: .wiki [mode] [degrees of separation]`
# e.g: .wiki dynamic 20, or .wiki random 0

# The [mode] specifies how generating is conducted. 
# Either [dynamic] - a crawl of wikipedia from a random start, 
# which may take up to 2 minutes - or random. 
# For dynamic mode, you then need to specify degrees of separation with a number (max 25).
# Random generation picks two articles at random.
# However, you still need to specify a second argument, but can do as 0 or None.
# This will be changed in future versions (hopefully)

@bot.command(pass_context=True)
async def wiki(ctx, arg1, arg2):

    global checkIfRunning

    if (checkIfRunning == False):
        checkIfRunning = True

        await ctx.send("The Wikipedia run generator may take a minute, or two...")

        if arg1 == "dynamic":
            if arg2 == None:
                degreesOfSeperation = 10
            else:

                # Number of iterations the crawl will do

                degreesOfSeperation = int(arg2)
                if degreesOfSeperation > 25:
                    await ctx.send("Maximum degrees of separation is 25")
                    degreesOfSeperation = 25

            # get first article (random)

            firstArticle = wikiRandom()
            buildLinks = []
            buildLinks.append(firstArticle)

            # Start crawling Wikipedia

            for x in range(0, degreesOfSeperation):
                try:
                    nextLink = wikiLinks(buildLinks[x])
                    randLink = (random.choice(nextLink))
                except:

                    # Some articles are dead end. This attempts to remove it, and choose another link.

                    try:
                        buildLinks.pop()
                        continue

                    # However, sometimes the first item is a dead end.

                    except:
                        await ctx.send("Wiki run generator failed, random article too obscure, please try again...")
                        checkIfRunning = False

                buildLinks.append(randLink)

            await ctx.send("Your starting page is : " + str(buildLinks[0]) + ", and your end page is: " + str(buildLinks[-1]))

        # For the Random arg

        elif arg1 == "random":
            randomFirst = wikiRandom()
            randomSecond = wikiRandom()
            await ctx.send("Your starting page is : " + str(randomFirst) + ", and your end page is: " + str(randomSecond))

        checkIfRunning = False
    elif (checkIfRunning == True):
        await ctx.send("BossAI is busy generating a run, try again later...")

# Help command

@bot.command(pass_context=True)
async def wikiHelp(ctx):
    await ctx.send("Usage: `.wiki [mode] [degrees of separation]`\ne.g: `.wiki dynamic 20`, or `.wiki random 0`\nThe `[mode]` specifies how generating is conducted.\nEither `[dynamic]` - a crawl of Wikipedia from a random start,\nwhich may take up to 2 minutes - or random.\nFor dynamic mode, you then need to specify degrees of separation with a number (max 25).\nRandom generation picks two articles at random.\nHowever, you still need to specify a second argument, but can do as 0 or None.")

bot.run(DISCORD_TOKEN)