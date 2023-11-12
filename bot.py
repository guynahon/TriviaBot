import logging
import bot_settings
from DB.parameters_dictionary import db_values as db_values
from storage import Storage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater, MessageHandler, Filters, CallbackQueryHandler,
)
from collections import Counter
import random

db = Storage("Trivia")

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

players = {}
questions_counter = Counter()
correct_counter = Counter()


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    welcome_text = "Hello!\nWelcome to the SuperDuperTriviaBot!"
    questions_counter[chat_id], correct_counter[chat_id] = 0, 0
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
    if option == "diff_easy":
        query.edit_message_text("Difficulty: Easy")
    elif option == "diff_medium":
        query.edit_message_text("Difficulty: Medium")
    elif option == "diff_hard":
        query.edit_message_text("Difficulty: Hard")
    noq_msg = "Choose number of questions"
    noq_key = noq_keyboard()
    context.bot.send_message(chat_id=chat_id, text=noq_msg, reply_markup=noq_key)


def noq_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    players[chat_id]["noq"] = option
    if option == "noq_5":
        query.edit_message_text("Number of Questions: 5")
    elif option == "noq_10":
        query.edit_message_text("Number of Questions: 10")
    elif option == "noq_15":
        query.edit_message_text("Number of Questions: 15")

    topic = db_values[players[chat_id]["topic"]]
    diff = db_values[players[chat_id]["difficulty"]]
    noq = db_values[players[chat_id]["noq"]]

    players[chat_id]["questions"] = db.get_list_of_questions(topic=topic, diff=diff, noq=noq)
    logger.info("success to import questions from db")

    question_msg = get_current_question(chat_id, context)
    qa_key = question_answers_keyboard(chat_id)
    context.bot.send_message(chat_id=chat_id, text=question_msg, reply_markup=qa_key)


def qa_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    if option == "qa_correct":
        correct_counter[chat_id] += 1
        query.edit_message_text(f"Question Number {questions_counter[chat_id] + 1}: Correct! ✅")
    else:
        query.edit_message_text(f"Question Number {questions_counter[chat_id] + 1}: Wrong! ❌")
    questions_counter[chat_id] += 1
    question_msg = get_current_question(chat_id, context)
    qa_key = question_answers_keyboard(chat_id)
    context.bot.send_message(chat_id=chat_id, text=question_msg, reply_markup=qa_key)


def end_game(chat_id, context):
    # TODO : update all-time-scoreboard
    # TODO : End game msg (current game score)
    chat_id = chat_id
    context.bot.send_message(chat_id=chat_id, text=f"You got {correct_counter[chat_id]} questions right out of {questions_counter[chat_id]}!")


def get_current_question(chat_id, context) -> str:
    try:
        return players[chat_id]["questions"][questions_counter[chat_id]]["question"]
    except IndexError:
        end_game(chat_id, context)


def get_current_answers(chat_id):
    answers = [[players[chat_id]["questions"][questions_counter[chat_id]]["correct_answer"], "qa_correct"],
               [players[chat_id]["questions"][questions_counter[chat_id]]["incorrect_answers"][0], "qa_wrong1"],
               [players[chat_id]["questions"][questions_counter[chat_id]]["incorrect_answers"][1], "qa_wrong2"],
               [players[chat_id]["questions"][questions_counter[chat_id]]["incorrect_answers"][2], "qa_wrong3"]]
    random.shuffle(answers)
    return answers


def topic_keyboard():
    keyboard = [
        [InlineKeyboardButton("⚽️ Sports ⚽️", callback_data=f"topic_sports"),
         InlineKeyboardButton("🏛️ History 🏛️", callback_data=f"topic_history")],
        [InlineKeyboardButton("🎮 Video Games 🎮", callback_data=f"topic_video_games"),
         InlineKeyboardButton("🎰 General Knowledge 🎰", callback_data=f"topic_general")],
        [InlineKeyboardButton("🎤 Music 🎤", callback_data=f"topic_music"),
         InlineKeyboardButton("🌍 Geography 🌍", callback_data=f"topic_geo")],
    ]
    return InlineKeyboardMarkup(keyboard)


def difficulty_keyboard():
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data=f"diff_easy"),
         InlineKeyboardButton("Medium", callback_data=f"diff_medium"),
         InlineKeyboardButton("Hard", callback_data=f"diff_hard")],
    ]
    return InlineKeyboardMarkup(keyboard)


def noq_keyboard():
    keyboard = [
        [InlineKeyboardButton("5", callback_data=f"noq_5"),
         InlineKeyboardButton("10", callback_data=f"noq_10"),
         InlineKeyboardButton("15", callback_data=f"noq_15")],
    ]
    return InlineKeyboardMarkup(keyboard)


def question_answers_keyboard(chat_id):
    answers = get_current_answers(chat_id)
    keyboard = [
        [InlineKeyboardButton(answers[0][0], callback_data=answers[0][1])],
        [InlineKeyboardButton(answers[1][0], callback_data=answers[1][1])],
        [InlineKeyboardButton(answers[2][0], callback_data=answers[2][1])],
        [InlineKeyboardButton(answers[3][0], callback_data=answers[3][1])]]
    return InlineKeyboardMarkup(keyboard)


my_bot = Updater(token=bot_settings.TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
# my_bot.dispatcher.add_handler(MessageHandler(Filters.text, on_text))
my_bot.dispatcher.add_handler(CallbackQueryHandler(topic_button, pattern="^topic_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(difficulty_button, pattern="^diff_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(noq_button, pattern="^noq_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(qa_button, pattern="^qa_"))

logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")

# def on_text(update: Update, context: CallbackContext):
#     chat_id = update.effective_chat.id
#     msg = update.message.text
#     logger.info(f"+ Got #{chat_id}: {msg!r}")
#     doc = db.add_item(chat_id, msg)
#     response = f"Added {msg!r}, cart has {len(doc['items'])}."
#     context.bot.send_message(chat_id=chat_id, text=response)
