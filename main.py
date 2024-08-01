import os
import dotenv
import random
import datetime
import typing

import discord
from discord.ext import commands
from discord import app_commands

dotenv.load_dotenv() # NOTE to set the token, create your own .env file, and add the line "token=YOUR_TOKEN_HERE"
TOKEN = os.getenv('token')
VERBOSE_MODE = os.getenv('verbose_mode', 'false').lower() == 'true' # NOTE set this to True to enable verbose logging mode

bot = commands.Bot(command_prefix='dnd ', help_command=None, intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} hybrid commands!')
    
    if VERBOSE_MODE:
        guilds = bot.guilds
        print(f'Connected to {len(guilds)} guilds!')
        for guild in guilds:
            print(f'  {guild.name} -> ({guild.id})')

@bot.hybrid_command(name="roll", description="Roll one or multiple dice") # TODO use a universal class for Dice in order to make future commands easier to implement
async def roll(ctx, die: str, count: int = 1, stat: str = None):
    if die in ['d100', 'd20', 'd12', 'd10', 'd8', 'd6', 'd4']: # check if the die type is valid
        pass
    else:
        await ctx.send("Invalid die type. Please use d4, d6, d8, d12, d20, or d100.")
        return
    sides = int(die[1:]) # grab the number of sides from the die type
    rolls = [random.randint(1, sides) for _ in range(count)] # roll the die the specified number of times

    stat_header = f" for {stat}" if stat != None else "" # REVIEW after implementing character sheets, deprecate this feature
    embed = discord.Embed(title=f"Rolling {count}d{sides}{stat_header}", description=f"{rolls} -> {sum(rolls)}") # CLEANUP this part is messy af
    for roll in enumerate(rolls):
        embed.add_field(name=f"Roll {roll[0] + 1}", value=roll[1], inline=False)
    embed.timestamp = datetime.datetime.now()
    embed.set_footer(text=f"ran by {ctx.author.name}", icon_url="https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png") # FIXME URL doesn't work
    
    await ctx.send(embed=embed)

@roll.autocomplete("die") # TODO review this
async def roll_autocompletion(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    data = []
    for die_choice in ['d100', 'd20', 'd12', 'd10', 'd8', 'd6', 'd4']:
        if current.lower() in die_choice.lower():
            data.append(app_commands.Choice(name=die_choice, value=die_choice))
    
    return data
    
bot.run(TOKEN)