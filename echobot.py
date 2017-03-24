import time
import json
import requests
import urllib
import pandas as pd
from sets import Set

TOKEN = "361459375:AAGhOyO58jWclIBYCGJOQXs6ixXTRJV835I"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
blood_data = pd.read_csv("C:\\Users\\Abhishek\\Hack In The North\\databases\\bloodbank.csv")
city_data = blood_data.ix[:,2]
city = Set(['Kolkata'])
for i in city_data:
    city.add(i)

city_list = list()
for i in city:
    city_list.append(i)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
    
def get_updates():
    url = URL + "getUpdates?timeout=100"
    js = get_json_from_url(url)
    return js
    
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    
    query = text
    #print type(query)
    #print type(city)
    p = ""
    f = 0
    for i in city_list:
        i = str(i)
        if i in query:
            for k in range(len(blood_data)):
                if i == blood_data.ix[k][2]:
                    #print type(blood_data.ix[k][5])
                    if str((blood_data.ix[k][5])) != "nan":
                        p = p + str((blood_data.ix[k][5])) + " \n"
                    f = 1
                        
    if f == 0:
        p = p + "Sorry! Incorrect Query"
    #print p
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (chat_id, p)
    
def send_message(chat_id, text):
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?chat_id={}&text={}".format(chat_id, text)
    get_url(url)

def main():
    last_textchat = (None, None)
    while True:
        #print("getting updates")
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            send_message(text, chat)
            last_textchat = (text, chat)
        time.sleep(0.05)

if __name__ == '__main__':
    main()
