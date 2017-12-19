# -*- coding: utf-8 -*-
__author__ = ["Tal Sayag", "Michal Kabra", "Omri Avisar"]

# imports:

import imageio
imageio.plugins.ffmpeg.download()
from InstagramAPI import InstagramAPI
import urllib
import cv2
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary# Logging into an account, to gain access to instagram

username = 'dana_aharonn'
password = 'iirastupido'
igAPI = InstagramAPI(username, password)
igAPI.login()


def get_data(username):
    igAPI.searchUsername(username)  # the only function which deals with username
    data = igAPI.LastJson
    print data

    user = data[u'user']
    id = user[u'pk']
    following = user[u'following_count']
    followers = user[u'follower_count']
    posts = user[u'media_count']
    img_url = user[u'hd_profile_pic_versions'][0][u'url']

    return [id, following, followers, posts, img_url]

def handle_img(url):
    '''
    download photo
    '''
    # urllib.urlretrieve(url, 'C:\Users\Administrator\insta_acc_pic.jpg')

    with open('C:\\Users\Administrator\\insta_acc_pic.jpg', 'wb') as handler:
        handler.write(img_data)
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary, executable_path='C:\geckodriver.exe')
    time.sleep(2)

    driver.get(url)

    input_username = driver.find_elements_by_xpath("//input[@name='username']")
    input_username.send_keys("username")

def find_face(image_path):
    '''
    checks if there is face in the profile pic
    '''
    casc_path = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(casc_path)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    print format(len(faces))
    if format(len(faces)) > 0:
        return True
    return False

    """# Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)"""


def identify(id, following, followers, posts, img_url):
    '''
    gives a rate of credibility
    '''
    max_per_one = 2
    rates = []
    rates.append(following_vs_followers(following, followers, max_per_one))  # 1
    rates.append(posting(posts, max_per_one))  # 2
    face = find_face(handle_img(img_url))
    if face is True:
        rates.append(6)
    else:
        rates.append(0)

    return sum_rate(rates)


def following_vs_followers(following, followers, max_per_one):
    rate = 0  # max = 2
    ratio = followers/following
    optimal = 0.33
    if ratio >= optimal:
        rate += max_per_one
    else:
        for x in xrange(1, 5):
            if ratio < 0.33-x*(0.33/4):
                max_per_one -= 0.5
        rate += max_per_one
    return rate


def posting(posts, max_per_one):
    rate = 0
    if posts >= 5:
        rate = max_per_one
    else:
        d_val = {'1': 0.4, '2': 0.8, '3': 1.2, '4': 1.6}
        rate = d_val[str(posts)]
    return rate


def sum_rate(num_list):
    rate = 0
    for num in num_list:
        rate += num
    return rate


def main():
    username = 'caradelevingne'
    [id, following, followers, posts, img_url] = get_data(username)
    print img_url
    identify(id, following, followers, posts, img_url)


if __name__ == '__main__':
    main()