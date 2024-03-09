# orderly_volume_boost_bot
simple bot to boost volume on orderly network for quest NFTs qualifying

# Orderly Trading Bot

This is a simple trading bot for the Orderly exchange.

## Setup

1. Clone this repository.
2. Install the required Python packages: `pip install python-dotenv requests pynacl`.
3. Create a `.env` file in the root directory of the project, and add your Orderly API keys:

```env
ORDERLY_KEY=your_orderly_key
ORDERLY_SECRET=your_orderly_secret
ACCOUNT_ID=your_account_id

Usage
Run the bot with python bot.py. The bot will prompt you to enter the trading pair and the trade size in USDC. It will then continuously create BUY orders and immediately close them with SELL orders of the same size.
or use the run.bat file
