import interactions  # Import the interactions.py library for Discord bot interactions
from interactions import *  # Import everything from interactions
from PIL import Image  # Import the PIL library for image processing
import qrcode as qr_lib  # Import the qrcode library for QR code generation
from io import BytesIO  # Import BytesIO for handling in-memory binary streams
import aiohttp  # Import aiohttp for asynchronous HTTP requests
import os  # Import os for environment variable access
import datetime  # Import datetime for date and time handling
import random  # Import random for generating random numbers
import asyncio  # Import asyncio for asynchronous programming

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Get the bot token from environment variables
token = os.getenv("TOKEN")

# Create a new bot instance with default intents
bot = Client(intents=Intents.DEFAULT, token=token)

@bot.event()
async def on_ready():
    """Event triggered when the bot is ready."""
    print(f"Logged in as {bot.user}")  # Log the bot's username
    print(f"Owned by {bot.owner}")  # Log the bot owner's username
    print("Bot is ready!")  # Indicate that the bot is ready to use

@slash_command(
    name="hello",
    description="Says hello"
)
async def hello(ctx: SlashContext):
    """Command that greets the user."""
    await ctx.send(f"Hello {ctx.author.mention}!")  # Send a greeting message mentioning the user

@slash_command(
    name="ping",
    description="Ping and get latency of the bot"
)
async def ping(ctx: SlashContext):
    """Command that returns the bot's latency."""
    pingembed = Embed(
        title="Pong!",  # Title of the embed
        description=f"{round(bot.latency * 1000)}ms",  # Calculate latency in milliseconds
        color=interactions.Color.random()  # Set a random color for the embed
    )
    await ctx.send(embeds=[pingembed])  # Send the embed as a response

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
@slash_option(
    name="color",
    description="Color of QR code",
    opt_type=OptionType.STRING,
    required=False
)
async def generate_qr(ctx: SlashContext, link: str, logo_url: str = None, color: str = None):
    """Command to generate a QR code with an optional logo."""
    # Generate QR code
    qr = qr_lib.QRCode(
        version=1,
        error_correction=qr_lib.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)  # Add the link or text to the QR code
    qr.make(fit=True)  # Optimize QR code size
    img = qr.make_image(fill_color="black", back_color="white" if fill_color is None else color).convert("RGB")  # Generate the QR code image
    
    # Add logo if provided
    if logo_url: 
        try:
            async with aiohttp.ClientSession() as session:    
                async with session.get(logo_url) as r:
                    r.raise_for_status()  # Raise an error for bad responses
                    logo_data = await r.read()  # Read the logo data
            # Load the logo image        
            logo = Image.open(BytesIO(logo_data))  # Open logo image
            qr_width, qr_height = img.size  # Get QR code dimensions
            logo_size = int(qr_width * 0.2)  # Resize logo to 20% of QR code width
            logo = logo.resize((logo_size, logo_size))  # Resize the logo

            # Calculate the position to paste the logo
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            img.paste(logo, logo_position, mask=logo if logo.mode == "RGBA" else None)  # Paste the logo onto the QR code
        except Exception as e:
            await ctx.send(f"An error occurred while fetching the logo: {str(e)}")  # Handle errors
            return

    # Prepare the QR code image for sending
    buffer = BytesIO()
    img.save(buffer, format="PNG")  # Save the image in PNG format
    buffer.seek(0)  # Move to the start of the BytesIO buffer

    file = File(file=buffer, file_name="qr.png")  # Create a file object for the image
    qrembed = Embed(
        title="QR Code",
        description=f"Here is your QR code for {link}",  # Description of the embed
    )
    qrembed.set_image(url="attachment://qr.png")  # Set the QR code image in the embed
    qrembed.set_footer(text=f"Requested by {ctx.author}\n {datetime.datetime.now()}")  # Footer with user info
    await ctx.send(embeds=qrembed, files=file)  # Send the embed and file

@slash_command(
    name="timer",
    description="Creates a random timer from 1 to 60 seconds"
)
async def timer(ctx: SlashContext):
    """Command to create a random timer between 1 and 60 seconds."""
    time = random.randint(1, 60)  # Generate a random time between 1 and 60 seconds
    tembed = Embed(
        title="Timer",
        description=f"Timer created for {time} seconds",  # Initial message
        color=interactions.Color.random()  # Set a random color for the embed
    )
    tembed.set_footer(text=f"Requested by {ctx.author}\n {datetime.datetime.now()}")  # Footer with user info
    msg1 = await ctx.send(embeds=tembed)  # Send the initial timer message
    await asyncio.sleep(time)  # Wait for the specified time

    # Create a new embed to notify that the timer has ended
    tembed_1 = Embed(
        title="Timer",
        description=f"Timer ended! \n {ctx.author.mention}",  # Notify user that the timer has ended
        color=interactions.Color.random()  # Set a random color for the embed
    )
    await msg1.edit(embeds=tembed_1)  # Edit the original message to indicate that the timer has ended
    print(f"{msg1} edited")  # Print to console for debugging

# Start the bot
bot.start()
