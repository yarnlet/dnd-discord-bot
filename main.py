import discord
from discord import app_commands

from enum import Enum
import random

MY_GUILD = discord.Object(id=1268010874694799511)  # replace with your guild id

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()

client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# dice roller

class DiceType(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    def __str__(self):
        return f'D{self.value}'
    def roll(self):
        return random.randint(1, self.value)

@client.tree.command()
@app_commands.describe(
    count='How many dice to roll.',
    dice_type='Which dice you want to roll.',
    modifier='Modifier is applied after all dice have been rolled.'
)
async def roll(interaction: discord.Interaction, count: int, dice_type: DiceType, modifier: int):
    """Says hello!"""
    embed=discord.Embed(
        title="Dice Roller",
        description=f'You rolled a {count}{dice_type} **{"+" if modifier >= 0 else "-"}{abs(modifier)}**. Let\'s see how it turned out',
        color=discord.Color.red()
        )
    dicestring = ""
    runningcount = 0
    for dicenum in range(count):
        runningcount += dice_type.roll()
        dicestring += f'Dice {dicenum + 1}: {dice_type.roll()}\n'
    embed.add_field(name="Dice Outcomes", value=dicestring, inline=False)
    embed.add_field(name="Dice Total", value=f'Base: {runningcount}\nWith Modifier: {runningcount} **{"+" if modifier >= 0 else "-"}{abs(modifier)}** = {runningcount + modifier}', inline=True)
    

    await interaction.response.send_message(embed=embed)
    # await interaction.response.send_message(f'Okay, you rolled {count}{dice_type}')


client.run(token)
