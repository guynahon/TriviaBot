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
                           "total_questions": noq}
        query = {"chat_id": chat_id}
        user_line = self.users.find_one(query)
        if user_line is None:
            self.users.insert_one(filter_criteria)
        else:
            new_correct = user_line["correct_answers"] + correct_answers
            new_total = user_line["total_questions"] + noq

            update_operation = {'$set': {'correct_answers': new_correct, 'total_questions': new_total}}

            self.users.update_one(query, update_operation)
