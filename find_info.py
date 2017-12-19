# -*- coding: utf-8 -*-
import pynder
import time
import sys

f = open("lastnames.txt")
LAST_NAMES = f.read()
f.close()

HEY = "היי"
OUTPUT_FILE = "result.txt"
FACEBOOK_ID = "100009292553127"
FACEBOOK_ACCESS_TOKEN = "EAAGm0PX4ZCpsBAMpclmSGjlkofwhvq9dZAmu0tXURfvAGv1R0O3JVOVBjwXQN83rOkZCITQvzr0oIOZB3VkR5acioe8yN2U0KFTNglONyZARtkBsQ4rR6KN1763qP0yIxKLi73i2JoCCTmT4OWtjn0UaEcKGtRoiW6ZCC6Am2V6VZA8RXQIMxtEZAJZCU2dWgtA3WpQBfbR7CmfkY5jgy0sjrAFCqm2vSLCH0ZCvvwvOXAPwZDZD"


def save_result_to_file(text):
    f = open(OUTPUT_FILE, "w")
    f.write(text)
    f.close()


def usage():
    print "Usage: python find_info.py <tinder name> [optional]"
    print "the bot will try to match a parallel instagram to the tinder profile"
    print "the bot will scan the biography and try to get the instagram profile if linked"
    print "if the last name is known it can be used and added as an optional argument"
    sys.exit(1)


def check_the_response(match):
    l = len(match.messages)
    while True:
        for message in match.messages:
            for word in message.split():
                if word in LAST_NAMES:
                    return word
        if len(match.messages) > l:
            return


def question_him_for_last_name(match):
    f = open("conv.txt", "r")
    lines = f.readlines()
    t = time.time()
    while True:
        if time.time() - 5000 > t:
            print "target not responding"
            sys.exit(1)
        for message in match.messages:
            if HEY in message:
                break
    match.message(lines.pop(0))  # send hey
    time.sleep(1)
    match.message(lines.pop(0))
    time.sleep(4)
    match.message(lines.pop(0))
    result = check_the_response(match)
    if result:
        return result
    match.message(lines.pop(0))
    match.message(lines.pop(0))
    f.close()
    result = check_the_response(match)
    if result:
        return result

    print "couldn't find the instagram user from the chat"
    sys.exit(1)


def check_if_username_exist(u):
    return u is not None


def find_intel(info, match):
    user = match.user
    username = user.instagram_username
    if check_if_username_exist(username):
        return username
    name = user.name
    last_name = ""
    if info:
        last_name = info[0]
    if last_name == "":
        last_name = question_him_for_last_name(match)
    if last_name:
        return find_instagram_user(name, last_name)
    return None


def main(name, more_info):
    session = pynder.Session(facebook_token=FACEBOOK_ACCESS_TOKEN, facebook_id=FACEBOOK_ID)
    matches = session.matches()
    for match in matches:
        if str(match.user.name) == name:
            result = find_intel(more_info, match)
            if result:
                if result[1]:
                    print "succeeded at revealing the instagram "
                    save_result_to_file(result)
            print "couldn't find the last name"
            return
    print "you haven't made contact with", name


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        l = sys.argv[1:]
        n = l.pop(0)
        main(n, l)
    else:
        main("Georgi", [])
        #usage()
