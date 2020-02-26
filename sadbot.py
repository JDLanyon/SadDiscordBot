import discord
import discord.emoji
from discord.ext import tasks, commands
import random
import json

# admin list
admins = json.load(open("private.json", 'r'))["admins"] # change to a list of user ids.

client = commands.Bot(command_prefix = ":(", case_sensitive = True)


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = ":("))
    print("Bot online.")


# on messages
@client.event
async def on_message(message):
    # avoid reponding to the bot's own messages
    if message.author == client.user:
        return
    
    global admins # get admin list
    
    # if messages occur in DMs
    if isinstance(message.channel, discord.DMChannel):
        # send responses to big boi users
        for admin_id in admins:
            user = client.get_user(int(admin_id))
            await user.send('`' + str(message.author.name) + " -> bot:` " + str(message.content))

    # print to terminal
    print(str(message.author.name) + " -> bot: " + str(message.content))

    # if someone says sex it's funny.
    if "sex" in str(message.content).lower():
        await message.channel.send("haha ***S H E X***")

    # don't say words (shut down messages relating to affection)
    with open("data.json", 'r') as f:
        data = json.load(f)
    blacklist = data["shutdowns"]["blacklist"]
    responses = data["shutdowns"]["responses"]
    # if message contains a blacklist word
    if [ele for ele in blacklist if(ele in str(message.content).lower())]:
        # send a random response
        response = random.choice(responses)
        print("bot -> " + str(message.author.name) + ": " + response) # print response
        await message.channel.send(response)
    # continue to listen for commands
    await client.process_commands(message)


# message someone
@client.command()
async def msg(ctx, target, text):
    global admins
    # check ur privlig
    if ctx.author.id not in admins:
        await ctx.send("You're not admin.")
        return

    # try to get the user id and send a message
    try:
        # print neato magneto bot sending context in terminal
        print("bot -> " + str(client.get_user(int(target)).name) + ": " + text)
        await ctx.send("`bot -> " + str(client.get_user(int(target)).name) + "`: " + text)

        # send text to the person with *id*
        user = client.get_user(int(target))
        await user.send(text)

    # if not, say you can't.
    except AttributeError:
        await ctx.send("The user must share a discord with the bot in order to be messaged sadly.")


@client.command(name="roast", aliases=["insult"])
async def roast(ctx, user=None):

    # roast yourself if no arguments are given.
    if user is None:
        user = ctx.author.mention

    # load insults
    insults = json.load(open("data.json", 'r'))["insults"]

    # send response
    response = str(user) + ", you " + random.choice(insults) + ' ' + random.choice(insults) + ' ' + random.choice(insults)
    print("bot -> " + str(user) + ": " + response) # print response
    await ctx.send(response)


# OWNER ONLY

# Get list of connected servers
@client.command()
async def servers(ctx):
    if ctx.author.id != admins[0]:
        await ctx.send("You can't do that, only the owner can do that.")
        return
    await ctx.send(f"Connected on {str(len(client.guilds))} servers:")
    await ctx.send('\n'.join(server.name for server in client.guilds))


# Terminate the bot via command
@client.command(name="terminate", aliases=["off", "disconnect"])
async def terminate(ctx):
    if ctx.author.id != admins[0]:
        await ctx.send("You can't terminate the bot, only the owner can.")
        return
    await ctx.send("k np, bye.")
    exit()


token = json.load(open("private.json", 'r'))["token"]
client.run(token)
