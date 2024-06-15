# Telegram Bot Setup

Rename `.env` to `.secretenvv`.

1. **Create a Bot via BotFather:**
   - Visit [BotFather](https://telegram.me/BotFather) on Telegram.
   - Follow the instructions to create your bot.
   - Obtain your bot's API token.
   - Change update the token in your `.secretenv` file.

2. **Set Bot Commands:**
   - Use `/setcommands` in BotFather to define your bot's commands.

# SIA Bot Configuration

1. **Configure Thresholds:**
   - Set thresholds for balance and storage in `config.py`.

2. **Database Setup:**
   - The default database is SQLite. To use another database, set `DEVELOPMENT` to `False` in `config.py` and provide a `DATABASE_URL`.

# Using the SIA Bot

1. **Add the Bot as a Contact:**
   - Add your bot on Telegram.

2. **Explore Commands:**
   - Access all available commands via the left burger-menu.

3. **Functions:**
   - Subscribe/unsubscribe to events.
   - Check balance and more.

# Extending the SIA Bot

1. **Add New Events:**
   - Extend the bot by adding new events for users to subscribe to.

2. **Monitor Pending Contracts Example:**
   - Use the endpoint: [HostD API - Monitor Pending Contracts](https://api.sia.tech/hostd#87d43895-9980-466b-ba2b-c874af67217b).
   - Integrate the API-request in `sia_handler.py`.

3. **Add Threshold Logic:**
   - Implement threshold logic in `main.py`.
   - (You can copy and adapt the existing logic from other calls/thresholds.)
