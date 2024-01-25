import discord
from discord import app_commands
import yaml
import os
from typing import Optional
import subprocess

# load config
config = None
with open(os.path.join(os.path.dirname(__file__), 'config.yaml')) as f:
    config = yaml.safe_load(f)
# create client
intents = discord.Intents.default()


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, guild_id):
        super().__init__(intents=intents)
        self.guild = discord.Object(id=guild_id)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=self.guild)
        await self.tree.sync(guild=self.guild)
        print('Setup complete.')


client = MyClient(intents=intents, guild_id=config["discord"]["guild_id"])
pal_process = None


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
@app_commands.describe()
async def pal_start(interaction: discord.Interaction):
    """start palworld server"""
    global pal_process
    if pal_process == None:
        pal_process = subprocess.Popen(config["palworld"]["path"], shell=True)
        await interaction.response.send_message(f'Palworld server started.')
    else:
        await interaction.response.send_message(f'Palworld server already running. If you cannot connect, try restarting the server.')


@client.tree.command()
@app_commands.describe()
async def pal_stop(interaction: discord.Interaction):
    """stop palworld server"""
    global pal_process
    if not pal_process == None:
        pal_process.kill()
        pal_process = None
        await interaction.response.send_message(f'Palworld server stopped.')
    else:
        await interaction.response.send_message(f'Palworld server not running.')

@client.tree.command()
@app_commands.describe()
async def pal_restart(interaction: discord.Interaction):
    """restart palworld server"""
    global pal_process
    if not pal_process == None:
        pal_process.kill()
        pal_process = None
    pal_process = subprocess.Popen(config["palworld"]["path"], shell=True)
    await interaction.response.send_message(f'Palworld server restarted.')

# run bot
client.run(config["discord"]["token"])
