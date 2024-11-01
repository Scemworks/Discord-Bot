# Discord Bot using interactions.py

A Discord bot built with the `interactions.py` library that provides various commands, including greeting users, checking latency, generating QR codes, and creating timers.

## Features

- **Hello Command**: Greet users with a personalized message.
- **Ping Command**: Check the bot's latency.
- **QR Code Generator**: Create QR codes from text or links, with optional logo support.
- **Random Timer**: Set a random timer between 1 and 60 seconds and get notified when it ends.
- **Programming Jokes**: Random programming jokes fetched using [jokeapi](https://sv443.net/jokeapi/v2/)

## Prerequisites

- Python 3.8 or higher
- A Discord bot token
- Required Python packages

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Scemworks/Discord-Bot.git
   cd Discord-Bot
   ```

2. **Install required packages**:

   You can create a virtual environment and install the required packages using `pip`:

   ```bash
   python -m venv venv
   source venv/bin/activate
   # If using fish instead of bash use source ```venv/bin/activate.fish```
   # On Windows use ```venv/bin/Activate.ps1```
   pip install -r requirements.txt
   ```
   
3. **Set up environment variables**:

   Create a `.env` file in the root of your project and add your Discord bot token:

   ```plaintext
   TOKEN="your_bot_token_here"
   ```


### How to Get a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on **New Application** and give your bot a name.
3. Navigate to **Bot** on the left sidebar and click **Add Bot**.
4. Under **Token**, click **Reset Token** to reveal it. Copy the token securely.
5. Store the token in your environment file as mentioned above in **`Step 3`**

This token is necessary for authenticating the bot on Discord.

## Usage

1. **Run the bot**:

   Ensure you are in the project directory and your virtual environment is activated. Then run:

   ```bash
   python main.py
   ```
   in Linux
   ```bash
   python3 main.py
   ```

3. **Use commands**:

   - **/hello**: The bot will greet you.
   - **/ping**: Get the latency of the bot.
   - **/qr**: Generate a QR code from a link or text (optional: include a logo).
     - Example: `/qr link:https://example.com logo_url:https://example.com/logo.png`
   - **/timer**: Set a random timer from 1 to 60 seconds.
   - **/joke**: Get a random programming joke 
## Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [interactions.py](https://github.com/interactions-py/interactions.py) - A powerful library for building Discord bots.
- [Pillow](https://python-pillow.org/) - Python Imaging Library for image processing.
- [qrcode](https://pypi.org/project/qrcode/) - Library for generating QR codes.
