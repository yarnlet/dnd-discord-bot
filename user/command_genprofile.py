import json
import discord

import os
from os import path

CWD = os.getcwd()
DB = path.join(CWD, 'database')

async def genprofile_command(ctx, user: discord.User):
    if not path.exists(path.join(DB, str(user.id))):
        os.mkdir(path.join(DB, str(user.id)))
        with open(path.join(DB, str(user.id), 'profile.json'), 'w') as f:
            json.dump({
                'name': user.name,
                'id': user.id,
                'avatar': user.avatar.url,
                'created_at': user.created_at.strftime('%Y-%m-%d_%H:%M:%S'),
                'profile': 'This user has not set their profile yet.'
            }, f, indent=4)
        await ctx.send(f'Profile created for {user.name}!')
    else:
        await ctx.send(f'Profile already exists for {user.name}!')
    