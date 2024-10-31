import interactions
from interactions import *
from PIL import Image
import qrcode as qr_lib
from io import BytesIO
import aiohttp
import os
import datetime
import random
import asyncio

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
    name="hello",
    description="Says hello"
)
async def hello(ctx: SlashContext):
    await ctx.send(
        f"Hello {ctx.author.mention}!"
)

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

@slash_command(
    name="qr",
    description="Generate a QR code from given text/link and add logo if specified"
)
@slash_option(
    name="link",
    description="Link/text to generate QR code from",
    opt_type=OptionType.STRING,
    required=True
)
@slash_option(
    name="logo_url",
    description="URL of logo to add to QR code",
    opt_type=OptionType.STRING,
    required=False
)
async def generate_qr(ctx: SlashContext, link: str, logo_url: str = None):
    # Generate QR code
    qr = qr_lib.QRCode(
        version=1,
        error_correction=qr_lib.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    
    # Add logo if provided
    if logo_url: 
        try:
            async with aiohttp.ClientSession() as session:    
                async with session.get(logo_url) as r:
                    r.raise_for_status()  # Raise an error for bad responses
                    logo_data = await r.read()
            # Load the logo image        
            logo = Image.open(BytesIO(logo_data))
            qr_width, qr_height = img.size
            logo_size = int(qr_width * 0.2)  # Resize logo to 20% of QR code width
            logo = logo.resize((logo_size, logo_size))

            # Calculate the position to paste the logo
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, logo_position, mask=logo if logo.mode == "RGBA" else None)
        except Exception as e:
            await ctx.send(f"An error occurred while fetching the logo: {str(e)}")
            return

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    file = File(file=buffer, file_name="qr.png")
    qrembed = Embed(
        title="QR Code",
        description=f"Here is your QR code for {link}",
    )
    qrembed.set_image(url="attachment://qr.png")
    qrembed.set_footer(text=f"Requested by {ctx.author}\n {datetime.datetime.now()}")
    await ctx.send(embeds=qrembed, files=file)

#Random timer creator
@slash_command(
    name="timer",
    description="Creates a random timer"
)
async def timer(ctx: SlashContext):
    time = random.randint(1, 60)
    tembed = Embed(
        title="Timer",
        description=f"Timer created for {time} seconds",
        color=interactions.Color.random()
    )
    tembed.set_footer(text=f"Requested by {ctx.author}\n {datetime.datetime.now()}")
    await ctx.send(embeds=tembed)
    await asyncio.sleep(time)
    tembed = Embed(
        title="Timer",
        description=f"Timer ended {ctx.author.mention}",
        color=interactions.Color.random()
    )
    #await ctx.send(embeds=tembed)
bot.start()
