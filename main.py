import discord
from discord.ext import commands
from discord import app_commands

import os
import dotenv

import random
import datetime
import typing
from enum import Enum

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
# dice roller

# TODO please put these two in separate files; i'd like to have a system where we create a new python file for a command, and have one python file for class defs and stuff
# this is why i like typescript more :/

class DiceType(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    def __str__(self):
        return f'd{self.value}'
    def roll(self):
        return random.randint(1, self.value)

@bot.hybrid_command(name="roll", description="Roll one or multiple dice")
@app_commands.describe(
    count='How many dice to roll.',
    dice_type='Which dice you want to roll.',
    modifier='Modifier is applied after all dice have been rolled.'
)
async def roll(ctx, count: int, dice_type: DiceType, modifier: int):
    embed=discord.Embed(
        title="Dice Roller",
        description=f'You rolled a {count}{dice_type} **{"+" if modifier >= 0 else "-"}{abs(modifier)}**. Let\'s see how it turned out',
        color=discord.Color.red()
        )
    dicestring = ""
    runningcount = 0
    rolls = [dice_type.roll() for _ in range(count)] # roll the die the specified number of times
    for dicenum in range(count):
        runningcount += rolls[dicenum]
        dicestring += f'Dice {dicenum + 1}: {rolls[dicenum]}\n'
    embed.add_field(name="Dice Outcomes", value=dicestring, inline=False)
    embed.add_field(name="Dice Total", value=f'Base: {runningcount}\nWith Modifier: {runningcount} **{"+" if modifier >= 0 else "-"}{abs(modifier)}** = {runningcount + modifier}', inline=True)
    embed.timestamp = datetime.datetime.now()

    embed.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar) # FIXME URL doesn't work

    await ctx.send(embed=embed)
    # await interaction.response.send_message(f'Okay, you rolled {count}{dice_type}')

bot.run(TOKEN)
