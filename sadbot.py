import discord
import discord.emoji
from discord.ext import tasks, commands
import random
import json
import os

# admin list
admins = json.load(open("private.json", 'r'))["admins"] # change to a list of user ids.
moderators = json.load(open("private.json", 'r'))["moderators"]

client = commands.Bot(command_prefix = ":(", case_sensitive = False)


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = ":("))
    print("Bot online.")


# ON MESSAGES
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
            await user.send(f"` {message.author.name} ({message.author.id}) -> bot:` " + str(message.content))

    # print to terminal
    print(str(message.author.name) + " -> bot: " + str(message.content))

    # if someone says sex it's funny.
    if "sex" in str(message.content).lower():
        await message.channel.send("haha ***SEX***")
    if "69" in str(message.content).lower():
        await message.channel.send("hehe 69")

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
        if target[0] == '<': # make sure target is only the client id.
            target = target[3:-1]
        user = client.get_user(int(target))
        print("bot -> " + str(user.name) + ": " + text)
        await ctx.send("`bot -> " + str(user.name) + "`: " + text)

        # send text to the person with *id*
        await user.send(text)

    except AttributeError:
        try:
            # try with fetch_user
            user = await client.fetch_user(int(target))
            print("bot -> " + str(user.name) + ": " + text)
            await ctx.send("`bot -> " + str(user.name) + "`: " + text)
            # send text to the person with *id*
            await user.send(text)

        except AttributeError:
            await ctx.send("Could not find that user sadly.")


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


# ADMINS AND MODS ONLY


# Shut down my PC
@client.command(name="shutdown")
async def ShutDown(ctx):
    if not(ctx.author.id in admins): # only admins and mods
        await ctx.send("You can't do that, only the bot admins / moderators can do that.")
        return
    await ctx.send("**SHUTTING DOWN YOUR PC**")
    os.system("shutdown /s /t 1")


# Get list of connected servers
@client.command(name="servers", aliases=["serverlist"])
async def Servers(ctx):
    if not(ctx.author.id in admins or ctx.author.id in moderators): # only admins and mods
        await ctx.send("You can't do that, only the bot admins / moderators can do that.")
        return
    await ctx.send(f"Connected on {str(len(client.guilds))} servers:")
    await ctx.send('\n'.join(server.name for server in client.guilds))

# Get list of moderators
@client.command(name="moderators", aliases=["modlist"])
async def Terminate(ctx):
    if not(ctx.author.id in admins or ctx.author.id in moderators): # only admins and mods
        await ctx.send("You can't do that, only the bot admins / moderators can do that.")
        return
    modlist = ""
    for member in moderators:
        try:
            modlist += f"{client.get_user(member)} ({member})\n"
        except:
            modlist += f"{member} (couldn't find user.)\n"
    await ctx.send(modlist)


# ADMINS ONLY

@client.command(name="addmod")
async def AddMod(ctx, id):
    if not(ctx.author.id in admins):
        await ctx.send("You can't do that, only the bot admins can do that.")
        return

    # for @ mentions
    if id[0] == '<':
        id = id[3:-1]
        print(id)
    try:
        # check if they're already a mod
        if int(id) in moderators:
            await ctx.send(f"{id} is already found in the moderator list.")
            return
        # add to mod list
        moderators.append(int(id)) # add client id
    except:
        await ctx.send("Invalid client id.")
        return
    # replace json with added moderator.
    f = open("private.json", "r")
    data = json.load(f)
    f.close()
    data["moderators"] = moderators
    f = open("private.json", "w")
    json.dump(data, f, indent=4)
    f.close()
    await ctx.send(f"Successfuly added {id}.")

@client.command(name="removemod")
async def removemod(ctx, id):
    if not (ctx.author.id in admins):
        await ctx.send("You can't do that, only the bot admins can do that.")
        return

    # for @ mentions
    if id[0] == '<':
        id = id[3:-1]
        print(id)
    try:
        # check if they're in the mod list
        if not(int(id) in moderators):
            await ctx.send(f"{id} is not found in the moderator list.")
            return
        moderators.remove(int(id))
    except:
        await ctx.send("Something went wrong, DM Sausytime#6969.")
        return
    # replace json with added moderator.
    f = open("private.json", "r")
    data = json.load(f)
    f.close()
    data["moderators"] = moderators
    f = open("private.json", "w")
    json.dump(data, f, indent=4)
    f.close()
    await ctx.send(f"Successfuly removed {id}.")

# OWNER ONLY
# Terminate the bot via command
@client.command(name="terminate", aliases=["off", "disconnect"])
async def terminate(ctx):
    if ctx.author.id != admins[0]:
        await ctx.send("You can't terminate the bot, only the bot owner can.")
        return
    await ctx.send("k np, bye.")
    exit()

@client.command(name="addadmin")
async def AddAdmin(ctx, id):
    if not(ctx.author.id in admins[0]):
        await ctx.send("You can't do that, only the bot owner can do that.")
        return

    # for @ mentions
    if id[0] == '<':
        id = id[3:-1]
        print(id)
    try:
        # check if they're already a mod
        if int(id) in admins:
            await ctx.send(f"{id} is already found in the admin list.")
            return
        # add to mod list
        moderators.append(int(id)) # add client id
    except:
        await ctx.send("Invalid client id.")
        return
    # replace json with added moderator.
    f = open("private.json", "r")
    data = json.load(f)
    f.close()
    data["admins"] = admins
    f = open("private.json", "w")
    json.dump(data, f, indent=4)
    f.close()
    await ctx.send(f"Successfuly added {id}.")


token = json.load(open("private.json", 'r'))["token"]
client.run(token)
