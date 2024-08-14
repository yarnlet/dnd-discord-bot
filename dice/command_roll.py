import discord
from discord import app_commands
import datetime
import typing

from classes import DiceType

# roll command
async def roll_command(ctx, count: int, dice_type: DiceType, modifier: int=0):
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

    embed.set_footer(text=f"Ran by {ctx.author.name}", icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)
