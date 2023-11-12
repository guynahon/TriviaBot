import logging
import bot_settings
from storage import Storage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater, MessageHandler, Filters, CallbackQueryHandler,
)

db = Storage("shopping_cart")

WELCOME_TEXT = "Welcome to our bot!"

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

players = {}


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    welcome_text = "Hello!\nWelcome to the SuperDuperTriviaBot!"
    topic_key = topic_keyboard()
    context.bot.send_message(chat_id=chat_id, text=welcome_text)
    topic_msg = "To play, pick a topic"
    context.bot.send_message(chat_id=chat_id, text=topic_msg, reply_markup=topic_key)


def topic_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    players[chat_id] = {}
    players[chat_id]["topic"] = option
    if option == "topic_sports":
        query.edit_message_text("Topic: Sports")
    elif option == "topic_history":
        query.edit_message_text("Topic: History")
    elif option == "topic_video_games":
        query.edit_message_text("Topic: Video Games")
    elif option == "topic_general":
        query.edit_message_text("Topic: General Knowledge")
    elif option == "topic_music":
        query.edit_message_text("Topic: Music")
    elif option == "topic_geo":
        query.edit_message_text("Topic: Geography")
    diff_msg = "Choose difficulty"
    diff_key = difficulty_keyboard()
    context.bot.send_message(chat_id=chat_id, text=diff_msg, reply_markup=diff_key)


def difficulty_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    players[chat_id]["difficulty"] = option
    print(players[chat_id])
    if option == "diff_easy":
        query.edit_message_text("Difficulty: Easy")
    elif option == "diff_medium":
        query.edit_message_text("Difficulty: Medium")
    elif option == "diff_hard":
        query.edit_message_text("Difficulty: Hard")


# def on_text(update: Update, context: CallbackContext):
#     chat_id = update.effective_chat.id
#     msg = update.message.text
#     logger.info(f"+ Got #{chat_id}: {msg!r}")
#     doc = db.add_item(chat_id, msg)
#     response = f"Added {msg!r}, cart has {len(doc['items'])}."
#     context.bot.send_message(chat_id=chat_id, text=response)

def topic_keyboard():
    keyboard = [
        [InlineKeyboardButton("Sports", callback_data=f"topic_sports"),
         InlineKeyboardButton("History", callback_data=f"topic_history")],
        [InlineKeyboardButton("Video Games", callback_data=f"topic_video_games"),
         InlineKeyboardButton("General Knowledge", callback_data=f"topic_general")],
        [InlineKeyboardButton("Music", callback_data=f"topic_music"),
         InlineKeyboardButton("Geography", callback_data=f"topic_geo")],
    ]
    return InlineKeyboardMarkup(keyboard)


def difficulty_keyboard():
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data=f"diff_easy"),
         InlineKeyboardButton("Medium", callback_data=f"diff_medium"),
         InlineKeyboardButton("Hard", callback_data=f"diff_hard")],
    ]
    return InlineKeyboardMarkup(keyboard)


my_bot = Updater(token=bot_settings.TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
# my_bot.dispatcher.add_handler(MessageHandler(Filters.text, on_text))
my_bot.dispatcher.add_handler(CallbackQueryHandler(topic_button, pattern="^topic_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(difficulty_button, pattern="^diff_"))

logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
