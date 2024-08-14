import json
import discord

import os
from os import path

CWD = os.getcwd()
DB = path.join(CWD, 'database')

async def userinfo_command(ctx, user: discord.User):
    if path.exists(path.join(DB, str(user.id), 'profile.json')):
        with open(path.join(DB, str(user.id), 'profile.json'), 'r') as f:
            profile = json.load(f)
            embed=discord.Embed(
                title="User Profile",
                description=f'Profile for {profile["name"]} (ID: {profile["id"]})',
                color=discord.Color.red()
                )
            embed.add_field(name="Profile", value=profile['profile'], inline=False)
            embed.set_thumbnail(url=profile['avatar'])
            embed.timestamp = discord.utils.parse_time(profile['created_at'])
            await ctx.send(embed=embed)
    else:
        await ctx.send(f'Profile does not exist for {user.name}!')