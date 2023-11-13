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
![bot_intro](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/ba922ffe-b324-4cb4-94d8-2c93c8fd2077)

Bot start:
![bot_start](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/5163cac9-5144-4b8c-aebd-ad18cc0732a5)

Bot rules:
![bot_rules_score](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/ab486c41-0425-4081-b555-58d313111d69)

Bot leaderboard:
![bot_leaderboard](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/36f3f056-ce2a-4a34-a386-16cf8ca444fa)

Bot menu:
![bot_menu](https://github.com/grurniClasses/telegram-bot-hackathon-superduperteam/assets/143611810/a83ff261-de38-4a61-862a-4cc46a833ba9)



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
