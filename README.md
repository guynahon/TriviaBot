# Super Duper Trivia Bot

## The Team
- Guy Nahon
- Dor Matania
- Aysel Yarahmedov

## About this bot

Super Duper Trivia Bot is an interactive bot by Super Duper Team!
Using this bot you can challenge yourself with varying difficulty levels and categories.
Our bot will keep score of your right answers in this game and all games to come, to create personalized game statistics and a leaderboard.
Admins can add specific questions to the database through the bot itself.

t.me/super_duper_trivia_bot

Bot intro:

![bot_intro copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/dff9d0b2-1270-4308-a691-c0a507caba62)

Bot start:

![bot_start copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/9b188228-91d6-4114-81ac-3b33445682e4)

Question examples:

![first_question copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/7b7987c9-f8af-43c6-9687-8000d7c36104)

![second_question copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/a9a59f9a-6fac-45bc-bbe2-bec29636ddc4)

![wrong_answer copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/476ef984-95f2-4702-b429-6a3c47997588)


Bot rules:

![bot_rules_score copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/baeedc0e-7d62-4494-9810-13b7848d201a)

Bot leaderboard:

![bot_leaderboard copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/5f138512-95c2-4cdf-b492-7118fff2e00b)

For admins: Add Question

![add_question copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/475b530d-b69e-4dcb-bfea-b58f16aa02cd)

![add_question_proccess copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/872040d2-8199-4a52-96c8-9974efb4ae34)

Add Question without authorization:

![no_permission copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/dba1d0a2-613a-4074-b117-619822c898a1)

Bot menu:

![bot_menu copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/66c797e9-56b9-450d-83a8-941b63d16cc9)



## Instructions for Developers 
### Prerequisites
- Python 3.11
- Poetry
- MongoDB

### Setup
- git clone this repository 
- cd into the project directory
- Install dependencies:
      poetry install
      install MongoDB
- Upload database into MongoDB


- Get an API Token for a bot via the [BotFather](https://telegram.me/BotFather)
- Create a `bot_settings.py` file with your bot token:

      BOT_TOKEN = 'xxxxxxx'

### Running the bot        
- Run the bot:

      poetry run python bot.py
