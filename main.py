from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import settings
from src._telegram.commands import COMMANDS
import src._telegram.commands as commands
from src.database.session import get_session



if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

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
    
    application.run_polling()