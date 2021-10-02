import discord
from discord.ext import commands
import os
import asyncio
import aiohttp
import json
import math
from config import digital_ocean_link, bot_token
from datetime import datetime


from restaurant_mappings import name_mappings
# import discord_tools.tools as tools


bot = commands.Bot(command_prefix='-', activity = discord.Activity(type=discord.ActivityType.watching, name="Restaurant Wait Times"))

async def get_confirmation(msg, member):
    id = member.id
    valid_reactions = ["✅","❌"]
    for i in valid_reactions:
        await msg.add_reaction(i)
    try:
        reaction, _user = await bot.wait_for(
            'reaction_add',
            timeout=60,
            check=lambda reaction, user: str(reaction.emoji) in valid_reactions and user.id == id and reaction.message.id == msg.id
        )
    except asyncio.TimeoutError:
        timeup_embed = msg.embeds[0]
        timeup_embed.set_footer(text="No longer accepting input")
        timeup_embed.color = 0xFF0000
        await msg.edit(embed=timeup_embed)
        return False
    else:
        if str(reaction.emoji) == "✅":
            return True
        elif str(reaction.emoji) == "❌":
            return False

@bot.event
async def on_ready():
    print("bot started")

@bot.command(aliases = ['line', 'lines'])
async def get_restaurant_times(ctx):
    # data = {i:i+1 for i in range(26)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{digital_ocean_link}/send') as response:
            data = await response.text()

    # print(data)
    data = json.loads(data)
    data = [(i, data[i]) for i in data]
    data.sort(key = lambda x: x[1])

    embed = discord.Embed(
        title = f"Currently Open Restaurants - Sorted by Waiting Time",
        colour = discord.Color.green()
    )
    # print(data)
    entries = 0
    for i in data:
        temp = ''
        if i[1] > 1:
            temp = f'{i[1]//1} minutes '
        embed.add_field(name = f'{name_mappings[str(i[0])]}', value = f'{temp}{round((i[1]%1)*60, 2)} seconds')
        if entries == 12:
            break

    await ctx.send(embed = embed)

started = {}

@bot.command(aliases = ['in'])
async def start_recording_time(ctx, *, id):

    if not id.isdigit():
        for i in name_mappings:
            if id.upper() in name_mappings[i]:
                id = i
                break
        
    if not id.isdigit():
        id = "0"

    started[ctx.author.id] = (datetime.now(), id)
    # print(started[ctx.author.id])
    res_name = name_mappings[str(id)]
    embed = discord.Embed(
        title = f"Started Marking Time for {res_name}",
        colour = discord.Color.green(),
        description = f"Started measuring your wait time for {res_name}"
    )
    for i in os.listdir("logos"):
        if i.startswith(str(id) + '.'):
            file = discord.File(f"logos/{i}", filename = i)
            embed.set_image(url=f"attachment://{i}")
    

    await ctx.reply(file=file, embed = embed)

@bot.command(aliases = ['out'])
async def stop_recording_time(ctx):
    if ctx.author.id not in started:
        embed = discord.Embed(
            title = f"You didn't start recording time.",
            colour = discord.Color.red(),
        )
        await ctx.send(embed = embed)
        return
    
    start_time = started[ctx.author.id][0]
    now = datetime.now()

    res_id = started[ctx.author.id][1]
    res_name = name_mappings[res_id]

    wait_time = now - start_time
    started.pop(ctx.author.id)
    seconds = wait_time.total_seconds()

    if math.floor(seconds/60) > 1:
        temp = f"{math.floor(seconds/60)} minutes, "
    else:
        temp = ""
    embed = discord.Embed(
        title = f"Would you like to submit the wait time for {res_name}",
        colour = discord.Color.green(),
        description = f"Recorded Wait Time is{temp} {int(seconds) % 60} seconds"
    )

    mesg = await ctx.send(embed = embed)
    answer = await get_confirmation(mesg, ctx.author)

    if not answer:
        embed = discord.Embed(
            title = f"Time Not Submitted",
            colour = discord.Color.red(),
        )
        await ctx.reply(embed = embed)
        return
    
    embed = discord.Embed(
        title = f"Times Submitted to Server",
        colour = discord.Color.green(),
    )
    await ctx.send(embed = embed)

    async with aiohttp.ClientSession() as session:
        data = {
            'res_id': int(res_id),
            'wait_time': seconds/60,
        }
        await session.post(f'{digital_ocean_link}/submit', json = data)
    

bot.run(bot_token)