# Telegram Setup

You need to setup the Bot via Botfather (https://telegram.me/BotFather),

then send the botfather a list with your commands `/setcommands` and follow instructions.

# SIA BOT Setup

You need to setup the Treshholds for your Balance and Storage in `config.py`. The project is running on a `sqllite` db by default but can be exchanged if changing the `DEVELOPMENT` var in `config.py` to `False`, you'd then also need to provide a `DATABASE_URL`. 

# SIA Bot Usage

You basically just have to text the bot (add it as a contact), from there on you'll see all available commands in the left burger-menu. You can subscribe/unsubscribe to events, check the balance and some other things.

# SIA Bot Extension

This project aims for collaborators, it's beeing built to be easily extenable. It basically needs to add an event to which a user can subscribe and the HostD-API-Call and a Treshhold.

For instance:

** Monitor pending contracts ** 

We'd need this endpoint:
https://api.sia.tech/hostd#87d43895-9980-466b-ba2b-c874af67217b

And integrate the call in `sia_handler.py`. The class is easily extenable. 

The Treshhold Logic has to be added then to `main.py`. The logic can basically copied and adopted from the other calls/treshholds.