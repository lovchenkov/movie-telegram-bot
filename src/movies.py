import requests
import re
from constants import *
import json


class Person(object):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def display(self):
        return self.name + ' ' + IMDB_LINK + "name/" + self.id


class Movie(object):
    def __init__(self, movie: str):
        try:
            req_data = requests.get(API_LINK + "SearchTitle/" + API + movie).json()["results"][0]
            self.id = req_data["id"]
            self.picture_link = req_data["image"]
            self.data = requests.get(API_LINK + "FullCast/" + API + self.id).json()
        except Exception:
            raise NameError

    def get_movie_name(self):
        return self.data["fullTitle"]

    def get_movie_link(self) -> str:
        return IMDB_LINK + "title/" + self.data["imDbId"]

    def get_directors(self) -> list:
        directors = []
        for dir in self.data["directors"]["items"]:
            directors.append(Person(dir["id"], dir["name"]))
        return directors

    def get_actors(self):
        actors = []
        for actor in self.data["actors"]:
            actors.append(Person(actor["id"], actor["name"]))
        return actors

    def get_description(self) -> tuple:  # returns pair (description, trailer link)
        results = requests.get(API_LINK + "Trailer/" + API + self.id).json()
        return results["videoDescription"], results["link"]

    def get_metacritic_reviews(self) -> tuple:  # returns pair of best and worst rated reviews
        results = requests.get(API_LINK + "MetacriticReviews/" + API + self.id).json()
        if len(results["items"]) == 0:
            raise SyntaxError
        return results["items"][0], results["items"][-1]

    def get_picture_link(self) -> str:
        return self.picture_link


def find_common_actors(movie1: str, movie2: str) -> list:
    try:
        actors1 = Movie(movie1).get_actors()
        actors2 = Movie(movie2).get_actors()
    except NameError:
        raise NameError
    else:
        common_actors = []
        for actor1 in actors1:
            for actor2 in actors2:
                if actor1.id == actor2.id:
                    common_actors.append(actor1)
        return common_actors


def display_review(review):
    return review["publisher"] + ", " + review["author"] + ", rating: " + review["rate"] + "\n" + review["content"]