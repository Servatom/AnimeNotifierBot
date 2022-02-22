import discord
from discord.ext import commands
from functionality import datascrape, utils
from database import SessionLocal, engine
import models
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup')
    async def setup(ctx):
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
        guild = db.query(models.Clients).filter(models.Clients.guild_id == guild_id).first()
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
            client = models.Clients(guild_id, channel.id, prefix)
            db.add(client)
            db.commit()
            prefix_data[str(guild_id)] = client.prefix
        await channel.send("Setup complete")