import interactions
from interactions import *

import os

from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")

bot = Client(intents=Intents.DEFAULT, token=token)

@bot.event()
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Owned by {bot.owner}")
    print("Bot is ready!")

@slash_command(
    name="ping",
    description="Ping and get latency of the bot"
)
async def ping(ctx: SlashContext):
    pingembed = Embed(
        title="Pong!",
        description=f"{round(bot.latency * 1000)}ms",
        color=interactions.Color.random()
    )
    await ctx.send(embeds=[pingembed])

bot.start()