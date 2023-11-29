import telebot
from telebot import types
from movies import *
import urllib
bot = telebot.TeleBot('6261255874:AAHEyyDrVPiSlb7KCfl8-nI_aAXFUKbXDYE')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("help")
    btn2 = types.KeyboardButton("movie")
    btn3 = types.KeyboardButton("common actors")
    btn4 = types.KeyboardButton("description")
    btn5 = types.KeyboardButton("reviews")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Привет!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def process(message):
    if message.text in {"help", "/help"}:
        bot.send_message(message.from_user.id, "/movie -- see information about the movie\n"
                                               "/common -- see all common actors for two movies\n"
                                               "/description -- see short description and trailer\n"
                                               "/reviews -- see some of MetaCritic reviews.")
    elif message.text in {"movie", "/movie"}:
        bot.send_message(message.from_user.id, "What movie are you interested in?")
        bot.register_next_step_handler(message, display_movie)
    elif message.text in {"common actors", "/common"}:
        bot.send_message(message.from_user.id, "What two movies are you interested in? (format is movie1 # movie2)")
        bot.register_next_step_handler(message, display_movies_intersection)
    elif message.text in {"reviews", "/reviews"}:
        bot.send_message(message.from_user.id, "What movie are you interested in?")
        bot.register_next_step_handler(message, display_reviews)
    elif message.text in {"description", "/description"}:
        bot.send_message(message.from_user.id, "What movie are you interested in?")
        bot.register_next_step_handler(message, display_description)
    else:
        bot.send_message(message.from_user.id, "I don't understand you. Use /help to see all available options.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("help")
    btn2 = types.KeyboardButton("movie")
    btn3 = types.KeyboardButton("common_actors")
    btn4 = types.KeyboardButton("description")
    btn5 = types.KeyboardButton("reviews")
    markup.add(btn1, btn2, btn3, btn4, btn5)


def display_reviews(message):
    try:
        movie = Movie(message.text)
    except NameError:
        output_message = "Seems like this movie doesn't exist."
    else:
        reviews = movie.get_metacritic_reviews()
        output_message = display_review(reviews[0]) + '\n\n' + display_review(reviews[1])
    bot.send_message(message.from_user.id, output_message)


def display_movie(message):
    try:
        movie = Movie(message.text)
    except NameError:
        output_message = "Seems like this movie doesn't exist."
    else:
        output_message = movie.get_movie_name() + '\n' + movie.get_movie_link() + '\n'

        """"adding info about directors"""
        output_message += "Directors:" + '\n'
        dir_counter = 0
        for dir in movie.get_directors():
            output_message += dir.display() + '\n'
            dir_counter += 1
            if dir_counter >= MAX_DIRECTORS_NUM:
                break
        output_message += "...\n"

        """"adding info about actors"""
        output_message += '\n' + "Actors:" + '\n'
        actor_counter = 0
        for actor in movie.get_actors():
            output_message += actor.display() + '\n'
            actor_counter += 1
            if actor_counter >= MAX_ACTORS_NUM:
                break
        output_message += "...\n"

        """sending picture of movie"""
        url = movie.get_picture_link()
        f = open('../dist/out.jpg', 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        img = open('../dist/out.jpg', 'rb')
        bot.send_photo(message.from_user.id, img)
        img.close()

    bot.send_message(message.from_user.id, output_message)


def display_movies_intersection(message):
    try:
        movie1, movie2 = message.text.split('#')
    except ValueError:
        bot.send_message(message.from_user.id, "You didn't follow the format.")
        return

    try:
        common_actors = find_common_actors(movie1, movie2)
    except NameError:
        output_message = "Seems like one of these movies doesn't exist."
    else:
        if len(common_actors) == 0:
            bot.send_message(message.from_user.id, "Oops! There are no common actors")
            return
        output_message = "Commons actors are\n"
        actor_counter = 0
        for actor in common_actors:
            output_message += actor.display() + '\n'
            actor_counter += 1

    bot.send_message(message.from_user.id, output_message)


def display_description(message):
    try:
        movie = Movie(message.text)
    except NameError:
        output_message = "Seems like this movie doesn't exist."
    else:
        description, trailer_link = movie.get_description()
        output_message = description + "\n" + trailer_link
        bot.send_message(message.from_user.id, output_message)


bot.polling(none_stop=True, interval=0)

