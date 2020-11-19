import json
import time
from modules import mtwitter, google
from datetime import date
from database import database


def twitterController(query, maximum):
    response = mtwitter.twitterSearch(query, maximum)

    if response == -1:
        return -1

    object = {
        "source": "Twitter",
        "content": response
    }

    twitterJson = object
    return twitterJson

# def instagramController():


def googleController(query, maximum):
    response = google.googleCommentsSearch(query, maximum)

    if response == -1:
        return -1

    object = {
        "source": "Google Comments",
        "content": response
    }

    googleJson = object
    return googleJson


def exec(query, maximum, note):
    try:
        init = time.time()
        print('Twitter crawling started...')
        twitterComments = twitterController(query, int(maximum))
        # googleComments = googleController(query, int(maximum)/4)

        comments = []

        comments.append(twitterComments) if twitterComments is not -1 else []
        # comments.append(googleComments) if googleComments is not -1 else []

        end = time.time()
        executionTime = end - init

        newData = {
            'note': note,
            'query': query,
            'maximum': maximum,
            'comments': comments,
            'date': date.today().strftime("%d/%m/%Y"),
            'time': executionTime
        }

        collection = database.collection()

        _id = collection.insert(newData)

        return str(_id)
    except Exception as ex:
        print(ex)
        return 0
