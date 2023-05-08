import os
import eel
import requests
import wolframalpha
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from duckduckgo_search import ddg

eel.init(".")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:       
        print("Listening query...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing query...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
    return query

def textToSpeech(response) :
    print("Converting text to speech...")
    myobj = gTTS(response)
    myobj.save("response.mp3")

@eel.expose
def speak() :
    playsound(os.path.dirname(__file__) + '/response.mp3')

def clean(result) :
    temp = result['body'].split('.')
    i = 0
    while (i < len(temp)) :
        if (temp[i] == '') :
            del(temp[i])
        else :
            i += 1
    if len(temp) > 1 :
        del(temp[-1])
    temp = '.'.join(temp)
    temp += '.'
    return temp

def wolfram(query) :
    print("Processing query...")
    client = wolframalpha.Client('E8UU7K-L6R82ALXXR')
    res = client.query(query)
    response = next(res.results).text
    if response == '(data not available)' :
        raise Exception
    textToSpeech(response)
    return response

def chatGPT (query) :
    print("Generating result...")
    url = "https://chatgpt-gpt-3-5.p.rapidapi.com/ask"
    payload = { "query": query }
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "44ebac729amsh6248873c84ca2e1p1a1644jsn9adb1b12dbbe",
	    "X-RapidAPI-Host": "chatgpt-gpt-3-5.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers).json()['response']
    textToSpeech(response)
    return response

def ddg_search(query) :
    print("Almost there, hold on a sec...")
    results = ddg(query)
    response = clean(results[0])
    textToSpeech(response)
    return response

def news(query) :
    print("Fetching news...")
    url = "https://bing-news-search1.p.rapidapi.com/news/search"
    querystring = {"q":query, "count":"1", "freshness":"Day", "textFormat":"Raw", "safeSearch":"Off"}
    headers = {
	    "content-type": "application/octet-stream",
	    "X-BingApis-SDK": "true",
	    "X-RapidAPI-Key": "44ebac729amsh6248873c84ca2e1p1a1644jsn9adb1b12dbbe",
	    "X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com"
    }
    result = requests.get(url, headers=headers, params=querystring).json()
    response = result['value'][0]['name'] + '. ' + result['value'][0]['description']
    textToSpeech(response)
    return response

@eel.expose
def queryHandler(enteredQuery) :
    if 'news' in enteredQuery :
        try :
            return news(enteredQuery)
        except :
            try :
                return ddg_search(enteredQuery)
            except :
                return "I'm sorry, please try again."
    else :
        try :
            return wolfram(enteredQuery)
        except :
            try :
                return chatGPT(enteredQuery)
            except :
                try :
                    return ddg_search(enteredQuery)
                except :
                    return "I'm sorry, please try again."
eel.start("index.html", size=(900, 700))