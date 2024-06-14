import asyncio
import nest_asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from config import settings
from src._telegram.commands import COMMANDS
import src._telegram.commands as commands
from src.database.session import get_session
from src.sia.sia_handler import SiaHostdHandler
from src.database.models import User, Event


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
        database = get_session()
        # metrics = await hostd_handler.get_metrics_information()
        # mock metrics
        metrics = {"balance": 10}
        # get all events of type balance
        event = database.query(Event).filter_by(event_name="balance").first()
        if event:
                balance = metrics.get('balance', None)
                print(balance)
                print(settings.BALANCE_TRESHHOLD)
                if balance and balance < settings.BALANCE_TRESHHOLD:
                    subscribers = event.subscribers
                    for subscriber in subscribers:
                        # send the alert to the subscriber
                        await application.bot.send_message(chat_id=subscriber.id, text="Balance treshhold hit")
        # get all alerts
        # alerts = await hostd_handler.get_alerts()
        # mock alert
        alerts = [
            {
                "id": "h:db6be3723a3c5c5d6a83b5448a606a429f5ec62700c678627c55b6a449c9f565",
                "severity": "info",
                "message": "Volume initialized",
                "data": {
                "elapsed": 186111899,
                "volumeID": 2
                },
                "timestamp": "2023-06-02T22:33:14.921184149Z"
            }
        ]

        # get all event subsriber with including their alerts severity settings
        for alert in alerts:
            # the event description maps the severity
            event = database.query(Event).filter_by(event_description=alert['severity']).first()
            if event:
                subscribers = event.subscribers
                for subscriber in subscribers:
                    # send the alert to the subscriber
                    await application.bot.send_message(chat_id=subscriber.id, text=alert['message'])
                
                # dismiss alert
                if settings.ALERTS_DISMISS_AFTER_SENDING:
                    # await hostd_handler.dismiss_alert(alert['id'])
                    pass



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
