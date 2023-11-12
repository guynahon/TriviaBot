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


