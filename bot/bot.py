from discord.ext import commands
import discord
import os
import models
from database import engine, SessionLocal
import asyncio

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)

prefix_data = {}

def fillPrefix():
    global prefix_data
    prefix_data = {}
    guilds = db.query(models.Server).all()
    for guild in guilds:
        prefix_data[str(guild.guild_id)] = guild.prefix
    
def get_prefix(client, message):
    global prefix_data
    prefix = ""
    try:
        prefix = os.environ['PREFIX']
    except:
        prefix = "*"
    print(prefix)
    try:
        prefix_guild = prefix_data[str(message.guild.id)]
    except:
        prefix_guild = prefix
    return prefix_guild

bot = commands.Bot(command_prefix=(get_prefix), help_command=None)

def getToken():
    return os.environ.get('TOKEN')


cogs = ['cogs.add', 'cogs.remove', 'cogs.notify', 'cogs.scraper']


def load_cogs():
    for cog in cogs:
        bot.load_extension(cog)


@bot.event
async def on_ready():
    print('AnimeNotifier is connected to Discord!')

@bot.command("setup")
async def setup(ctx):
    global prefix_data
    prefix = ""
    try:
        prefix = os.environ['PREFIX']
    except:
        prefix = "*"
    # get guild id
    guild_id = ctx.guild.id
    # get all channels of the server
    channels = ctx.guild.text_channels
    list_of_channels = []
    for channel in channels:
        if channel.permissions_for(ctx.guild.me).send_messages:
            list_of_channels.append(channel)
    # embed
    embed = discord.Embed(title="Setup", description="Please select a channel to send messages to", color=0x00ff00)
    count = 1
    for channel in list_of_channels:
        embed.add_field(name= str(count) +". " + channel.name, value=channel.id, inline=False)
        count = count + 1
    # send embed
    msg = await ctx.send(embed=embed)

    # get response
    def check(reply_user):
        return reply_user.author == ctx.author and reply_user.channel == ctx.channel

    # timeout error
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="No response",
            description=f"Waited for 60s no response received",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded for 60s so quitting!")
        return
    
    # check if response is valid
    channel_id = 0
    print(len(list_of_channels))
    try:
        channel_id = int(msg.content)
    except:
        print("here")
        embed = discord.Embed(
            title="Invalid response",
            description=f"{msg.content} is not a valid response",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded with a valid response so quitting!")
        return
    
    # check if channel is valid
    channel = list_of_channels[channel_id - 1]
    
    # check if guild id is already in database
    guild = db.query(models.Server).filter(models.Server.guild_id == guild_id).first()
    if guild:
        # update db
        guild.channel = channel.id
        db.commit()
        # send message
        embed = discord.Embed(
            title="Updated",
            description=f"Updated channel to {channel.name}",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    else:
        # create new client
        client = models.Server(guild_id, prefix, channel.id)
        db.add(client)
        db.commit()
        prefix_data[str(guild_id)] = client.prefix
    
    await channel.send("Setup complete")

@bot.command(name="prefix")
async def changePrefix(ctx):
    """
    Change the prefix of the bot
    """
    global prefix_data
    global prefix
    if str(ctx.guild.id) not in prefix_data:
            embed = discord.Embed(
                description="You are not registered, please run `" + prefix + "setup` first",
                title="",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
    prefix = db.query(models.Server).filter_by(guild_id=ctx.guild.id).first().prefix
    embed = discord.Embed(
        title="Enter the new prefix for your bot",
        description="Current prefix is : " + prefix,
    )
    await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=60
        )
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="Timed out",
            description="You took too long to respond",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    new_prefix = msg.content.strip()
    db.query(models.Server).filter_by(guild_id=ctx.guild.id).update(
        {"prefix": new_prefix}
    )
    try:
        db.commit()
    except Exception as e:
        print(e)
        await ctx.send("Something went wrong, please try again!")
        return
    embed = discord.Embed(
        title="Successfully updated prefix",
        description="Prefix changed to " + new_prefix,
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)

    # Update prefix_data and reload cogs
    prefix_data[str(ctx.guild.id)] = new_prefix

load_cogs()
fillPrefix()
bot.run(getToken())