import discord
from discord.ext import commands
from discord import app_commands

import os
import dotenv

import random
import datetime
import typing
from enum import Enum
from classes import DiceType

# commands (refactor if needed)
from dice.command_roll import roll_command
from dice.command_multiroll import multiroll_command

# usermanager commands (refactor if needed)
from user.command_genprofile import genprofile_command
from user.command_userinfo import userinfo_command

dotenv.load_dotenv() # NOTE to set the token, create your own .env file, and add the line "token=YOUR_TOKEN_HERE"
TOKEN = os.getenv('token')
VERBOSE_MODE = os.getenv('verbose_mode', 'false').lower() == 'true' # NOTE set this to True to enable verbose logging mode

bot = commands.Bot(command_prefix='dnd ', help_command=None, intents=discord.Intents.all()) # NOTE non slash commands are almost useless

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

@bot.hybrid_command(name="roll", description="Roll one or multiple dice")
@app_commands.describe(
    count='How many dice to roll.',
    dice_type='Which dice you want to roll.',
    modifier='Modifier is applied after all dice have been rolled.'
)
async def roll(ctx, count: int, dice_type: DiceType, modifier: int):
    await roll_command(ctx, count, dice_type, modifier) # SOURCE commands/command_roll.py

@bot.hybrid_command(name="multiroll", description="Roll one of 2-5 different dice")
@app_commands.describe(
    die1='The first type of dice to roll.',
    die2='The second type of dice to roll.',
    die3='The optional third type of dice to roll.',
    die4='The optional fourth type of dice to roll.',
    die5='The optional fifth type of dice to roll.',
    modifier='Modifier is applied after all dice have been rolled.'
)
async def multiroll(ctx, die1: DiceType, die2: DiceType, die3: DiceType=None, die4: DiceType=None, die5: DiceType=None, modifier: int=0):
    await multiroll_command(ctx, die1, die2, die3, die4, die5, modifier) # SOURCE commands/command_multiroll.py

# TODO might remove this
@bot.hybrid_command(name="genprofile", description="Generate a profile for a user")
@app_commands.describe(
    user='The user to generate a profile for.'
)
async def genprofile(ctx, user: discord.User):
    await genprofile_command(ctx, user)

@bot.hybrid_command(name="userinfo", description="Get a user's profile")
@app_commands.describe(
    user='The user to get the profile for.'
)
async def userinfo(ctx, user: discord.User):
    await userinfo_command(ctx, user)

bot.run(TOKEN)
