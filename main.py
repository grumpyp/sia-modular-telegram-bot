import asyncio
import nest_asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from config import settings
from src._telegram.commands import COMMANDS
import src._telegram.commands as commands
from src.database.session import get_session
from src.sia.sia_handler import SiaHostdHandler

nest_asyncio.apply()

commands_list = [
    BotCommand("start", "Start the bot"),
    BotCommand("cancel", "Cancel the current operation"),
    BotCommand("help", "Show help message"),
    BotCommand("listcommands", "List all commands"),
    BotCommand("listevents", "List all events"),
    BotCommand("cancelevent", "Cancel an event subscription"),
    BotCommand("subscriptions", "Show your subscriptions"),
    BotCommand("balance", "Check your balance"),
    BotCommand("register", "Register for an event"),
]

async def poll_sia_hostd(application):
    hostd_url = settings.HOSTD_URL
    hostd_username = settings.HOSTD_USERNAME
    hostd_password = settings.HOSTD_PASSWORD
    hostd_handler = SiaHostdHandler(hostd_url, hostd_username=hostd_username, hostd_password=hostd_password)
    
    while True:
        # accounts_info = await hostd_handler.get_accounts()
        wallet_info = await hostd_handler.get_wallet_information()
        print(wallet_info)

        # Example threshold check
        # PSEUDO CODE
        """        if wallet_info['balance'] < settings.BALANCE_THRESHOLD:
            await application.bot.send_message(chat_id=settings.ADMIN_CHAT_ID, text=f"Low balance alert: {wallet_info['balance']}")
        """
        await asyncio.sleep(settings.POLL_INTERVAL)  # Poll every defined interval

async def main():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Set commands for the bot menu
    await application.bot.set_my_commands(commands_list)

    # db handler also used to setup models on start
    db = get_session()
    
    # Common
    start_handler = CommandHandler('start', commands.start)
    cancel_handler = CommandHandler('cancel', commands.cancel)
    help_handler = CommandHandler('help', commands.help)
    list_commands_handler = CommandHandler('listcommands', commands.list_commands)
    list_events_handler = CommandHandler('listevents', commands.list_events)
    cancel_event_handler = CommandHandler('cancelevent', commands.cancel_subscription)
    show_subscriptions = CommandHandler('subscriptions', commands.show_subscriptions)
    unknown_handler = MessageHandler(filters.COMMAND, commands.unknown)

    # SIA related
    balance_handler = CommandHandler('balance', commands.balance)

    # register handler
    application.add_handler(start_handler)
    application.add_handler(cancel_handler)
    application.add_handler(help_handler)
    application.add_handler(list_events_handler)
    application.add_handler(cancel_event_handler)
    application.add_handler(show_subscriptions)
    application.add_handler(list_commands_handler)
    application.add_handler(balance_handler)
    
    # handles confirmation for the registration
    application.add_handler(CommandHandler('register', commands.handle_message))

    # this must be the last handler otherwise it doesn't recognize the others
    application.add_handler(unknown_handler)

    # Start the polling coroutine
    asyncio.create_task(poll_sia_hostd(application))
    
    # Run the application
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
