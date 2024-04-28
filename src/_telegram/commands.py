from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telegram import Update, ForceReply


COMMANDS = {
    'start': 'By using the start command your unique user information will be saved to our database to subscribe to events and more. by using /cancel you can delete your information',
    'help': 'Get help information',
    'listcommands': 'List all available commands',
    'balance': 'Check the balance for a given wallet on a specific network. Usage: `/balance <network> <wallet>`',
    'listevents': 'List all available events to subscribe',
    'register': 'Register to certain events event'
}


## Common
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # State management 
    #TODO: Use db here!
    USER_STATE = {}
    # State constants
    AWAITING_CONFIRMATION = 1

    user_id = update.effective_user.id
    # Set the user state to awaiting confirmation
    USER_STATE[user_id] = AWAITING_CONFIRMATION
    # Ask user to confirm
    await update.message.reply_text(
        "Please type 'confirm' to proceed.",
        reply_markup=ForceReply(selective=True)
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is an adaptable Telegram bot that seamlessly interfaces with Sia's API, offering users direct access to a variety of functionalities and data!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    text = update.message.text

    # Check if the user is in the confirmation state
    if USER_STATE.get(user_id) == AWAITING_CONFIRMATION:
        if text.lower() == 'confirm':
            # User confirmed, handle the confirmation
            await update.message.reply_text("Thank you for confirming! You're signed up. You can now sign up for events!")
            # Reset the state
            USER_STATE.pop(user_id, None)
        else:
            # Remind the user to confirm
            await update.message.reply_text("Registration failed. use /start to try again")
    else:
        # Normal message handling (if not in a special state)
        await update.message.reply_text("Send /start to begin!")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. To get an overview of commands please use /listcommands")

async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_list = "Available Commands:\n"
    # Generate a list of commands dynamically
    for command, description in COMMANDS.items():
        commands_list += f"/{command} - {description}\n\n"
    await update.message.reply_text(commands_list)


## SIA related

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract arguments from the command
    args = context.args
    if len(args) < 2:
        await update.message.reply_text('Please provide both network and wallet arguments like this: /balance <network> <wallet>')
        return
    network, wallet = args[0], args[1]
    # Print the arguments to the terminal
    print(f"Network: {network}, Wallet: {wallet}")
    await update.message.reply_text(f"Checking balance on {network} for wallet {wallet}...")