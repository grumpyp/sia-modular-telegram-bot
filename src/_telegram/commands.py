from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import Update, ForceReply
from src.database.session import get_session
from sqlalchemy.exc import IntegrityError

from src.database.models import User, Event


COMMANDS = {
    'start': 'By using the start command your unique user information will be saved to our database to subscribe to events and more. by using /cancel you can delete your information',
    'cancel': 'By using the cancel command you can delete your information from our database',
    'help': 'Get help information',
    'listcommands': 'List all available commands',
    'balance': 'Check the balance for a given wallet on a specific network. Usage: `/balance <network> <wallet>`',
    'listevents': 'List all available events to subscribe',
    'register': 'Register to certain events event',
    'subscriptions': 'List all subscriptions',
    'cancelevent': 'Cancel a subscription to an event',
}

# Get the database session
DB = get_session()

## Initial Sign Up
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is an adaptable Telegram bot that seamlessly interfaces with Sia's API, offering users direct access to a variety of functionalities and data!")
    user = update.effective_user
    # Check if user is already registered
    user_exists = DB.query(User.id).filter_by(id=user.id).first() is not None
    
    if user_exists:
        await update.message.reply_text("You're already signed up! Use /listevents to see available events.")
    else:
        # If not registered, add user to the database
        new_user = User(id=user.id, first_name=user.first_name, is_bot=user.is_bot, language_code=user.language_code, username=user.username)
        DB.add(new_user)
        DB.commit()
        await update.message.reply_text("You have been successfully signed up! Use /listevents to see available events or /help for more commands.")

# Cancel the registration
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Check if user is already registered
    user_exists = DB.query(User.id).filter_by(id=user.id).first() is not None
    
    if user_exists:
        # If registered, delete user from the database
        DB.query(User).filter_by(id=user.id).delete()
        DB.commit()
        await update.message.reply_text("You have been successfully removed from the database.")
    else:
        await update.message.reply_text("You're not signed up yet! Use /start to sign up.")

# List all available events
async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    events = DB.query(Event).all()
    event_list = "Available Events:\n"
    for event in events:
        event_list += f"{event.event_id} - {event.event_name}\n"
    await update.message.reply_text(event_list)

# Sign up to an event
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = DB.query(User).filter_by(id=user.id).first()

    if not db_user:
        await update.message.reply_text("User not found in the database.")
        return

    command_parts = update.message.text.split()
    if len(command_parts) < 2:
        await update.message.reply_text("Please provide an event ID!")
        return

    event_id = command_parts[1]
    event = DB.query(Event).filter_by(event_id=event_id).first()

    if not event:
        await update.message.reply_text("Event not found.")
        return

    # Debugging: Print current subscriptions before the operation
    print(f"User {db_user.id} current subscriptions before: {[e.event_id for e in db_user.events]}")

    # Check if user is already subscribed
    if event in db_user.events:
        await update.message.reply_text("You are already subscribed to this event.")
        return

    try:
        db_user.events.append(event)
        print(f"Attempting to register user {db_user.id} to event {event.event_id}")
        DB.commit()
        print(f"User {db_user.id} successfully registered to event {event.event_id}")
        await update.message.reply_text(f"Successfully registered to event {event.event_name}!")
    except IntegrityError as e:
        DB.rollback()
        print(f"IntegrityError: {e}")  # Debugging: Print the error message
        await update.message.reply_text("Failed to register for the event. It seems you are already subscribed.")
    finally:
        # Debugging: Print current subscriptions after attempting to register
        refreshed_user = DB.query(User).filter_by(id=user.id).first()  # Refresh the user object
        print(f"User {refreshed_user.id} current subscriptions after: {[e.event_id for e in refreshed_user.events]}")

    # Ensure the database session handling is correct
    DB.commit()

# Show all event subscriptions
async def show_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user = DB.query(User).filter_by(id=user.id).first()
    subscriptions = user.events
    if not subscriptions:
        await update.message.reply_text("You have no subscriptions yet. Use /listevents to see available events.")
        return
    subscription_list = "Your Subscriptions:\n"
    for event in subscriptions:
        subscription_list += f"{event.event_id} - {event.event_name}\n"
    await update.message.reply_text(subscription_list)

# Cancel an event subscription
async def cancel_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_in_db = DB.query(User).filter_by(id=user.id).first()
    if not user_in_db:
        await update.message.reply_text("You are not registered. Please use /start to register first.")
        return

    # Split the text to extract the event ID, if provided
    command_parts = update.message.text.split()
    if len(command_parts) < 2:
        await update.message.reply_text("Please provide an event ID to cancel your subscription.")
        return

    event_id = command_parts[1]
    event = DB.query(Event).filter_by(event_id=event_id).first()
    if event is None:
        await update.message.reply_text("Event not found.")
        return

    if event in user_in_db.events:
        user_in_db.events.remove(event)
        DB.commit()
        await update.message.reply_text(f"Successfully unsubscribed from event {event.event_name}!")
    else:
        await update.message.reply_text("You are not subscribed to this event.")


# Unknown command handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. To get an overview of commands please use /listcommands")

# List all available commands
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_list = "Available Commands:\n"
    # Generate a list of commands dynamically
    for command, description in COMMANDS.items():
        commands_list += f"/{command} - {description}\n\n"
    await update.message.reply_text(commands_list)

# Help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "Welcome to the bot! Here's how to get started:\n"
        "- Use /start to sign up and save your information in our database.\n"
        "- Once you're signed up, you can use /listcommands to see all available commands.\n\n"
        "Here are some other commands you might find useful:\n"
    )
    
    # Generate a list of additional commands dynamically, if desired
    for command, description in COMMANDS.items():
        if command not in ['start', 'listcommands']:  # Exclude start and listcommands to avoid redundancy
            help_message += f"/{command} - {description}\n"

    await update.message.reply_text(help_message)



## SIA related

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract arguments from the command
    args = context.args
    if len(args) < 2:
        await update.message.reply_text('Please provide both network and wallet arguments like this: /balance <network> <wallet>')
        return
    network, wallet = args[0], args[1]
    # SIA API Call
    
    await update.message.reply_text(f"Checking balance on {network} for wallet {wallet}...")