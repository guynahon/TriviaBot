from pymongo import MongoClient
import random


class Storage:
    def __init__(self, db_name, *, clear=False):
        client = MongoClient()
        if clear:
            client.drop_database(db_name)
        self.db = client.get_database(db_name)
        self.users = self.db.get_collection("Users")
        self.questions = self.db.get_collection("Questions")
        self.add_q = self.db.get_collection("new_q")

    def get_list_of_questions(self, topic, diff, noq):
        lst_of_questions = []
        filter_criteria = {"category": topic, "difficulty": diff}
        result = self.questions.find(filter_criteria)
        for i in result:
            lst_of_questions.append(i)
        random.shuffle(lst_of_questions)
        return lst_of_questions[:noq]

    def update_alltime_scoreboard(self, chat_id, correct_answers, noq, user_data):
        filter_criteria = {"chat_id": chat_id, "user_name": user_data["full_name"], "correct_answers": correct_answers,
                           "total_questions": noq, "games_played": 1, "user_level": 1}
        query = {"chat_id": chat_id}
        user_line = self.users.find_one(query)
        if user_line is None:
            self.users.insert_one(filter_criteria)
        else:
            new_correct = user_line["correct_answers"] + correct_answers
            new_total = user_line["total_questions"] + noq
            games_played = user_line["games_played"] + 1
            update_operation = {
                '$set': {'correct_answers': new_correct, 'total_questions': new_total, "games_played": games_played}}
            self.users.update_one(query, update_operation)

    def get_score(self, chat_id):
        query = {"chat_id": chat_id}
        user_line = self.users.find_one(query)
        if not user_line:
            return f"Play at least once to get a score!"

        return (f"Your total answered question number is: *{user_line['correct_answers']} "
                f"out of {user_line['total_questions']}*\nYour correct percentage is "
                f"*{(user_line['correct_answers']/user_line['total_questions'])*100}%*")

    def get_leaderboard(self):
        sort_criteria = [("correct_answers", -1)]
        result = self.users.find().sort(sort_criteria).limit(5)
        output = "🏆 *Leaderboard* 🏆\n"
        for i, line in enumerate(result, 1):
            if i == 1:
                output += f'*{i}. {line["user_name"]}, Score: {line["correct_answers"]}* 🥇\n'
            elif i == 2:
                output += f'*{i}. {line["user_name"]}, Score: {line["correct_answers"]}* 🥈\n'
            elif i == 3:
                output += f'*{i}. {line["user_name"]}, Score: {line["correct_answers"]}* 🥉\n'
            else:
                output += f'*{i}. {line["user_name"]}, Score: {line["correct_answers"]}*\n'
        return output

    def check_user_level(self, chat_id):
        query = {"chat_id": chat_id}
        user_line = self.users.find_one(query)
        if user_line is None:
            return 1
        return user_line["user_level"]

    def add_question_to_db(self, question_adder):
        topic = question_adder["topic"]
        diff = question_adder["difficulty"]
        question = question_adder["question"]
        correct = question_adder["correct_answer"]
        incorrect = question_adder["incorrect_answers"]
        question_to_db = {
            "category": topic,
            "type": "multiple",
            "difficulty": diff,
            "question": question,
            "correct_answer": correct,
            "incorrect_answers": incorrect
        }
        self.add_q.insert_one(question_to_db)
