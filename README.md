# Super Duper Trivia Bot

## The Team
- Guy Nahon
- Dor Matania
- Aysel Yarahmedov

## About this bot

Super Duper Trivia Bot is an interactive bot by Super Duper Team!
Using this bot you can challenge yourself with varying difficulty levels and categories.
Our bot will keep score of right answers in this game and all games to come together.

t.me/super_duper_trivia_bot

Bot intro:

![bot_intro copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/dff9d0b2-1270-4308-a691-c0a507caba62)

Bot start:

![bot_start copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/9b188228-91d6-4114-81ac-3b33445682e4)

Bot rules:

![bot_rules_score copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/baeedc0e-7d62-4494-9810-13b7848d201a)

Bot leaderboard:

![bot_leaderboard copy](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/5f138512-95c2-4cdf-b492-7118fff2e00b)

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
