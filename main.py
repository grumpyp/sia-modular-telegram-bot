from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import settings
from src._telegram.commands import COMMANDS
import src._telegram.commands as commands



if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Common
    start_handler = CommandHandler('start', commands.start)
    list_commands_handler = CommandHandler('listcommands', commands.list_commands)
    unknown_handler = MessageHandler(filters.COMMAND, commands.unknown)

    # SIA related
    balance_handler = CommandHandler('balance', commands.balance)


    # register handler
    application.add_handler(start_handler)
    application.add_handler(list_commands_handler)
    application.add_handler(balance_handler)
    
    # handles confirmation for the registration
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.handle_message))

    # this must be the last handler otherwise it doesn't recognize the others
    application.add_handler(unknown_handler)
    
    application.run_polling()