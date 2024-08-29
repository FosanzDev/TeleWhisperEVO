help = """
Command list:
---- BASIC COMMANDS ----
/start - Start the bot
/help - Show this message
/privacy - Show the privacy policy
"""

adminHelp = help + """

---- ADMIN COMMANDS ----
/ban - Ban a user
/unban - Unban a user
/banlist - Show the list of banned users
/setsuperuser - Set a user as superuser
/removesuperuser - Remove a user from the superuser list
/superuserlist - Show the list of superusers

You've been tagged as an admin.
This means you can use all commands.
"""

superuserHelp = help + """

You've been tagged as a superuser.
This means you can use the service for free until further notification.
"""

start = """
    Welcome to TeleWhisperEVO! 🤖 🚀
    
    This version of TeleWhisper is a complete rewrite of the original bot, with new features and improvements.
    For now, the bot will be FREE for everyone, but in the future, the classic paid mode will be available.
    
    WHY FREE? 🤔
    The bot is still in development, and I want to make sure everything works as intended before charging for it.
    Nevertheless, keeping up this is not cheap, so donations are always welcome. 🙏
    
    You can buy credits with the /buycredits command in @TeleWhisperBot and reserve them for the future paid mode. 🚀
    
    PAYPAL: https://paypal.me/FosanzDev 💳
    BUY ME A COFFEE: https://www.buymeacoffee.com/FosanzDev ☕
    
    Or with crypto:
    TON / NOT: UQDYvzCEWesgRPqs9Ft4UuzGo1L1EydHmziHfTJa-Mp3CS8b 🪙
    
    If I get enough donations, I'll be able to keep the bot free for longer. 🚀
    
    -------------------------
    Type /help for more info about the commands 📚
    -------------------------

    Please enjoy the bot and report any bugs to @Telewhispersupport. Thank you! 🙏
"""

privacy = """
This bot DOES NOT STORE:
- Your messages
- Any multimedia sent to the bot
- Any personal information (except your Telegram username and ID)

This bot DOES STORE:
- Your Telegram username and ID
- The amount of credits you have left
- The language you set for the translations
- The length of the audio you send to the bot (in case you want to get a refund for a failed transcription)

NOTE: The bot is still in development, so some features may not work as intended.For this reason there's a chance that the bot may store some of the data listed above. Cleanups will be performed every 5 minutes, so maximum data retention is 5 minutes.
"""

modeNote = """
___Select a mode from the options below:___\n
*Use free mode* - The bot will use the free mode, which is slower and less accurate, but free.\n
*Use paid mode* - The bot will use the paid mode, which is faster and more accurate, but costs 1 credit per second.
"""

errorMessage = """
An error occurred while processing your request.\nYou didn't get charged for this, just try again.\nIf the error persists, join @telewhispersupport for help.
"""