#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib.request


def generate_answers(quest, QuestionType):
    answers = []
    if QuestionType == "multiple":
        answers = [
            quest["correct_answer"],
            quest["incorrect_answers"][0],
            quest["incorrect_answers"][1],
            quest["incorrect_answers"][2]
        ]
        answers.sort()
    elif QuestionType == "boolean":
        answers = ["True", "False"]
    else:
        print("Unrecognized question type: " + QuestionType)
    return answers


def generate_questions(n, TOKEN, TOPIC, DIFFICULTY):
    QuestionURL = "https://opentdb.com/api.php?amount=" + \
        str(n) + "&token=" + TOKEN + TOPIC + DIFFICULTY

    with urllib.request.urlopen(QuestionURL) as url:
        data = json.loads(url.read().decode())
    return data


def get_token():
    TokenURL = "https://opentdb.com/api_token.php?command=request"

    with urllib.request.urlopen(TokenURL) as url:
        data = json.loads(url.read().decode())
        TOKEN = data["token"]
    return TOKEN

def get_topics():
    TopicURL = "https://opentdb.com/api_category.php"

    with urllib.request.urlopen(TopicURL) as url:
        data = json.loads(url.read().decode())
        topics = data["trivia_categories"]
    return topics
