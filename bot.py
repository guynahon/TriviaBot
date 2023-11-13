import logging
import bot_settings
from DB.parameters_dictionary import db_values as db_values
from DB.parameters_dictionary import add_values as add_values
from storage import Storage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from collections import Counter
import random
import time

db = Storage("Trivia")

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

players = {}
questions_counter = Counter()
correct_counter = Counter()
last_button_press_time_topic = {}
last_button_press_time_diff = {}
last_button_press_time_noq = {}
last_button_press_time_q = {}
question_adder = {"chat": False}


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    welcome_text = "*Hello!\nWelcome to the SuperDuperTriviaBot!*"
    questions_counter[chat_id], correct_counter[chat_id] = 0, 0
    players[chat_id] = {"correct_one": ""}
    topic_key = topic_keyboard()
    context.bot.send_message(
        chat_id=chat_id, text=welcome_text, parse_mode=ParseMode.MARKDOWN
    )
    topic_msg = "To play, pick a topic"
    context.bot.send_message(chat_id=chat_id, text=topic_msg, reply_markup=topic_key)


def score(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Getting score #{chat_id}")
    context.bot.send_message(
        chat_id=chat_id, text=db.get_score(chat_id), parse_mode=ParseMode.MARKDOWN
    )


def leaderboard(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Getting leaderboard #{chat_id}")
    context.bot.send_message(
        chat_id=chat_id, text=db.get_leaderboard(), parse_mode=ParseMode.MARKDOWN)


def rules(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"> Start rules #{chat_id}")
    rules_text = (
        f"*Hello {user.first_name}!*\n"
        f"*/start* -> to start a new game.\n"
        "*/score* -> to get your score statistics.\n"
        "*/leaderboard* -> to see the top 5 leading players.\n"
        "*/add_question* -> add a new question to the database (if you're an admin!).\n"
        "*just pick a topic, difficulty and number of questions and start playing!*"
    )
    context.bot.send_message(chat_id=chat_id, text=rules_text, parse_mode=ParseMode.MARKDOWN)


def topic_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_topic.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
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
    last_button_press_time_topic[chat_id] = current_time


def difficulty_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_diff.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
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
    last_button_press_time_diff[chat_id] = current_time


def noq_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_noq.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
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
    last_button_press_time_noq[chat_id] = current_time


def qa_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_q.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
    if option == "qa_correct":
        correct_counter[chat_id] += 1
        query.edit_message_text(f"Question Number {questions_counter[chat_id] + 1}: Correct! ✅")
    else:
        query.edit_message_text(
            f"Question Number {questions_counter[chat_id] + 1}: Wrong! ❌\n"
            f"*The correct answer is: {players[chat_id]['correct_one']}*",
            parse_mode=ParseMode.MARKDOWN,
        )
    questions_counter[chat_id] += 1
    if questions_counter[chat_id] < db_values[players[chat_id]["noq"]]:
        question_msg = get_current_question(chat_id, context)
        qa_key = question_answers_keyboard(chat_id)
        context.bot.send_message(chat_id=chat_id, text=question_msg, reply_markup=qa_key)
    else:
        end_game(chat_id, context, update)
    last_button_press_time_q[chat_id] = current_time


def end_game(chat_id, context, update):
    context.bot.send_message(
        chat_id=chat_id,
        text=f"*You got {correct_counter[chat_id]} questions right out of {questions_counter[chat_id]}!*",
        parse_mode=ParseMode.MARKDOWN,
    )
    db.update_alltime_scoreboard(
        chat_id=chat_id,
        correct_answers=correct_counter[chat_id],
        noq=questions_counter[chat_id],
        user_data=update.effective_user,
    )


def get_current_question(chat_id, context) -> str:
    return players[chat_id]["questions"][questions_counter[chat_id]]["question"]


def get_current_answers(chat_id):
    question_path = players[chat_id]["questions"][questions_counter[chat_id]]
    answers = [
        [question_path["correct_answer"], "qa_correct"],
        [question_path["incorrect_answers"][0], "qa_wrong1"],
        [question_path["incorrect_answers"][1], "qa_wrong2"],
        [question_path["incorrect_answers"][2], "qa_wrong3"],
    ]
    random.shuffle(answers)
    return answers


def topic_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⚽️ Sports ⚽️", callback_data=f"topic_sports"),
            InlineKeyboardButton("🏛️ History 🏛️", callback_data=f"topic_history"),
        ],
        [
            InlineKeyboardButton("🎮 Video Games 🎮", callback_data=f"topic_video_games"),
            InlineKeyboardButton("🎰 General 🎰", callback_data=f"topic_general"),
        ],
        [
            InlineKeyboardButton("🎤 Music 🎤", callback_data=f"topic_music"),
            InlineKeyboardButton("🌍 Geography 🌍", callback_data=f"topic_geo"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def difficulty_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Easy", callback_data=f"diff_easy"),
            InlineKeyboardButton("Medium", callback_data=f"diff_medium"),
            InlineKeyboardButton("Hard", callback_data=f"diff_hard"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def noq_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("5", callback_data=f"noq_5"),
            InlineKeyboardButton("10", callback_data=f"noq_10"),
            InlineKeyboardButton("15", callback_data=f"noq_15"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def question_answers_keyboard(chat_id):
    answers = get_current_answers(chat_id)
    for i in answers:
        if i[1] == "qa_correct":
            players[chat_id]["correct_one"] = i[0]
    keyboard = [
        [InlineKeyboardButton(answers[0][0], callback_data=answers[0][1])],
        [InlineKeyboardButton(answers[1][0], callback_data=answers[1][1])],
        [InlineKeyboardButton(answers[2][0], callback_data=answers[2][1])],
        [InlineKeyboardButton(answers[3][0], callback_data=answers[3][1])],
    ]
    return InlineKeyboardMarkup(keyboard)


def add_question(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = "Choose a topic: "
    context.bot.send_message(chat_id=chat_id, reply_markup=add_question_topic_keyboard(), text=text)


def add_topic_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_q.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
    if db.check_user_level(chat_id) == 2:
        question_adder["topic"] = add_values[option]
        if option == "add_topic_sports":
            query.edit_message_text("Topic: Sports")
        elif option == "add_topic_history":
            query.edit_message_text("Topic: History")
        elif option == "add_topic_video_games":
            query.edit_message_text("Topic: Video Games")
        elif option == "add_topic_general":
            query.edit_message_text("Topic: General Knowledge")
        elif option == "add_topic_music":
            query.edit_message_text("Topic: Music")
        elif option == "add_topic_geo":
            query.edit_message_text("Topic: Geography")
        context.bot.send_message(
            chat_id=chat_id,
            reply_markup=add_difficulty_keyboard(),
            text="Choose difficulty",
        )
    elif db.check_user_level(chat_id) == 1:
        logger.info("Not Authorized")
        query.edit_message_text(f"❌ You don't have the permission to add a questions ❌")


def add_difficulty_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    option = query.data
    question_adder["difficulty"] = add_values[option]
    question_adder["chat"] = True
    question_adder["counter"] = 0
    question_adder["incorrect_answers"] = []
    chat_id = update.effective_chat.id
    current_time = time.time()
    last_press_time = last_button_press_time_diff.get(chat_id, 0)
    if current_time - last_press_time < 1.3:
        return
    if option == "add_diff_easy":
        query.edit_message_text("Difficulty: Easy")
    elif option == "add_diff_medium":
        query.edit_message_text("Difficulty: Medium")
    elif option == "add_diff_hard":
        query.edit_message_text("Difficulty: Hard")
    last_button_press_time_diff[chat_id] = current_time
    context.bot.send_message(chat_id=chat_id, text="Enter a question")


def add_question_topic_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⚽️ Sports ⚽️", callback_data=f"add_topic_sports"),
            InlineKeyboardButton("🏛️ History 🏛️", callback_data=f"add_topic_history"),
        ],
        [
            InlineKeyboardButton(
                "🎮 Video Games 🎮", callback_data=f"add_topic_video_games"
            ),
            InlineKeyboardButton("🎰 General 🎰", callback_data=f"add_topic_general"),
        ],
        [
            InlineKeyboardButton("🎤 Music 🎤", callback_data=f"add_topic_music"),
            InlineKeyboardButton("🌍 Geography 🌍", callback_data=f"add_topic_geo"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def add_difficulty_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Easy", callback_data=f"add_diff_easy"),
            InlineKeyboardButton("Medium", callback_data=f"add_diff_medium"),
            InlineKeyboardButton("Hard", callback_data=f"add_diff_hard"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"Getting question from user #{chat_id}: {text!r}")

    if question_adder["chat"] and question_adder["counter"] < 5:
        if question_adder["counter"] == 0:
            question_adder["question"] = text
            context.bot.send_message(chat_id=chat_id, text="Enter the correct answer")

        elif question_adder["counter"] == 1:
            context.bot.send_message(chat_id=chat_id, text="Enter the Incorrect answer")
            question_adder["correct_answer"] = text

        elif question_adder["counter"] == 4:
            question_adder["incorrect_answers"].append(text)
            context.bot.send_message(chat_id=chat_id, text="*Question added to database!*",
                                     parse_mode=ParseMode.MARKDOWN)
            db.add_question_to_db(question_adder)
            logger.info("Added Question to DB")

        else:
            question_adder["incorrect_answers"].append(text)
            context.bot.send_message(chat_id=chat_id, text="Enter the Incorrect answer")

        question_adder["counter"] += 1

        if question_adder["counter"] == 5:
            question_adder["chat"] = False
            logger.info("Finished to get data from user")

    else:
        context.bot.send_message(chat_id=chat_id, text="Can not enter values.")


my_bot = Updater(token=bot_settings.TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
my_bot.dispatcher.add_handler(CommandHandler("score", score))
my_bot.dispatcher.add_handler(CommandHandler("leaderboard", leaderboard))
my_bot.dispatcher.add_handler(CommandHandler("rules", rules))
my_bot.dispatcher.add_handler(CommandHandler("add_question", add_question))
my_bot.dispatcher.add_handler(CallbackQueryHandler(topic_button, pattern="^topic_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(add_topic_button, pattern="^add_topic_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(difficulty_button, pattern="^diff_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(add_difficulty_button, pattern="^add_diff_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(noq_button, pattern="^noq_"))
my_bot.dispatcher.add_handler(CallbackQueryHandler(qa_button, pattern="^qa_"))
my_bot.dispatcher.add_handler(MessageHandler(Filters.text, respond))
logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
