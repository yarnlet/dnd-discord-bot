import discord
from discord import app_commands
import datetime

from classes import DiceType

# TODO character sheet helper, add more
async def genchar_command(ctx):
    response = await ctx.send("Generating a session for you...")
    
    # talk to server
    
    await response.edit(content="")