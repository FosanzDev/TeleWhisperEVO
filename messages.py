help = """
Command list:
---- BASIC COMMANDS ----
/start - Start the bot
/help - Show this message
/privacy - Show the privacy policy
/intro - Show the intro message

---- CREDIT COMMANDS ----
/credits - Show the credits you have left
/top_balance - Buy credits
/tip - Tip the developer
"""

intro = """
To start using the bot, you need to buy credits.
Type /top_balance to buy credits! 💳

Prices are as low as 0.0005€ per second of transcription! 🤑

Then, you can start sending any multimedia file to the bot and it will transcribe it for you! 🎉

If you have any questions, bug reporting, etc., feel free to ask in @Telewhispersupport. 🤗
"""

credits = "You have {} credits left!\nAdd more clicking -> /top_balance"

tip = """
Since fees are high, I would appreciate if you tip me over the following methods:

PAYPAL: https://paypal.me/FosanzDev 💳
BUY ME A COFFEE: https://www.buymeacoffee.com/FosanzDev ☕

Or with crypto:
TON / NOT: `UQDYvzCEWesgRPqs9Ft4UuzGo1L1EydHmziHfTJa-Mp3CS8b` 🪙

If I get enough donations, I'll be able to keep focus on adding new features and improving the bot. 🙏
"""

group_help = """
---- BASIC COMMANDS ----
/tw_help - Show this message
/tw_privacy - Show the privacy policy
/tw_credits - Show the credits you have left

If you want to top up your credits, use /top_credits in @tw_evo_bot
"""

superuserHelp = help + """

You've been tagged as a superuser.
This means you can use the service for free until further notification.
"""

start = """
Welcome to TeleWhisperEVO! 🤖 🚀
    
(EVO stands for EVOlution, as this is a complete rewrite of the original bot @TeleWhisperBot)

It works with groups now!

It now works with a new, faster and more accurate transcription service! 🎉

Start by clicking -> /intro to get used to the bot.

This bot is an omni-tool for Telegram, capable of:
    - Transcribing voice messages (With files up to 2GB 🤯 - tested up to 100MB ~ 2H audio file)
    - More coming soon! (type /coming_soon to see what's coming)

The bot is still in development, so some features may not work as intended. 🛠️
Inconveniences? Ideas? @Telewhispersupport. 🐞

If you want to support the development of the bot, you can donate to the developer with /tip. 🙏

-------------------------
Type /help for more info about the commands 📚
-------------------------

Please enjoy the bot and report any bugs to @Telewhispersupport. Thank you! 🙏
"""

coming_soon = """
Coming soon (from most to least priority):
- Translation of transcriptions (auto-detected language)
- Timestamping of transcriptions (srt format)
- Voice synthesis of any text (With a lot of voices and languages!)
- Explanation or summarization of the transcriptions
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
- A history of your interactions with the bot, including:
    - Actions: Length of the transcription and its cost with timestamps
    - Transactions: Amount of credits bought with timestamps

This history ensures I have enough info if something fails and you need help!

NOTE: The bot is still in development, so some features may not work as intended.For this reason there's a chance that the bot may store some of the data listed above. Cleanups will be performed every 5 minutes, so maximum data retention is 5 minutes.
"""

not_registered = """
You're not registered in the bot's database. Please type /start to register.
"""
