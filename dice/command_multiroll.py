import discord
from discord import app_commands
import datetime
import typing

from classes import DiceType

# multiroll command (1 and 2 are required, 3-5 are optional, allowing up to 5 different dice to be rolled)
async def multiroll_command(ctx, die1: DiceType, die2: DiceType, die3: DiceType=None, die4: DiceType=None, die5: DiceType=None, modifier: int=0):
    embed=discord.Embed(
        title="Multi Dice Roller",
        description=f'You rolled a multiple dice with **{"+" if modifier >= 0 else "-"}{abs(modifier)}**. Let\'s see how it turned out',
        color=discord.Color.red()
        )
    dicestring = ""
    runningcount = 0
    for index, die in enumerate([die1, die2, die3, die4, die5]):
        if die is not None:
            roll_outcome = die.roll()
            dicestring += f'Dice {index + 1} ({str(die)}): {roll_outcome}\n'
            runningcount += roll_outcome
    embed.add_field(name="Dice Outcomes", value=dicestring, inline=False)
    embed.add_field(name="Dice Total", value=f'Base: {runningcount}\nWith Modifier: {runningcount} **{"+" if modifier >= 0 else "-"}{abs(modifier)}** = {runningcount + modifier}', inline=True)
    embed.timestamp = datetime.datetime.now()

    embed.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)
