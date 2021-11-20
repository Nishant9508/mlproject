import pyttsx3  # pip install pyttsx3
import datetime
import time
import speech_recognition as sr  # pip install SpeechRecognition
import wikipedia  # pip install wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
from wikipedia.wikipedia import search
from bs4 import BeautifulSoup
import requests
import wolframalpha
import re
import sys

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

newVoiceRate = 180
engine.setProperty('rate', newVoiceRate)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def computational_intelligence(question):
    try:
        client = wolframalpha.Client('GWL394-2JYHWK299Q')
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except:
        speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
        return None


def startup():
    speak("Initializing alex")
    speak("Starting all systems applications")
    speak("Installing and checking all drivers")
    speak("Caliberating and examining all the core processors")
    speak("Checking the internet connection")
    speak("Wait a moment sir")
    speak("All drivers are up and running")
    speak("All systems have been activated")
    #speak("Now I am online")
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am alex. Online and ready sir. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en=in')
        print("You said : " + query)
    except Exception as e:
        print(e)
        speak("say that again please")
        return "None"

    return query


def time1():
    time1 = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The time right now is")
    speak(time1)
    print(time1)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("Today's date is")
    speak(date)
    speak(month)
    speak(year)
    print(date)
    print(month)
    print(year)


def cpu():
    usage = str(psutil.cpu_percent())
    speak("Cpu is at "+usage)
    print("Cpu is at "+usage)


    battery = psutil.sensors_battery()
    bat_percent = battery.percent
    speak("Battery is at ")
    speak(bat_percent) 
    speak("percent")
    print("Battery is at ") 
    print(bat_percent)
    print("percent")

def screenshot():
    img = pyautogui.screenshot()
    img.save(r'C:\Users\ASUS\Desktop\mlproject\ScreenShots\ss.png')


def jokes():
    speak(pyjokes.get_joke())


def myclass():
    time.sleep(2)
    wb.open_new('https://myclass.lpu.in/')

    time.sleep(4)

    pyautogui.press("tab")
    pyautogui.typewrite('11911126')
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.typewrite('')  # Idhar apna password daal lena
    pyautogui.press("enter")
    time.sleep(3)

    for i in range(5):
        pyautogui.press("tab")
    pyautogui.press("enter")
    time.sleep(2)
    # for k in range(15):  # for 1st class
    #     pyautogui.press("tab")
    # pyautogui.press("enter")
    # time.sleep(5)


def Temperature():
    city = query.split("in", 1)
    data = BeautifulSoup(requests.get(
        f"https://www.google.com/search?q=weather+in+{city [1]}").text, "html.parser")
    region = data.find("span", class_="BNeawe tAd8D AP7Wnd")
    temp = data.find("div", class_="BNeawe iBp4i AP7Wnd").text
    day = data.find("div", class_="BNeawe tAd8D AP7Wnd").text
    weather = day.split("m", 1)
    temperature = temp.split("C", 1)
    speak("Its Currently"+weather[1]+" and " +
          temperature[0]+"celcuis"+"in"+region.text)
    print("Its Currently"+weather[1]+" and " + temperature[0]+" celcuis "+"in "+region.text)      

if __name__ == "__main__":

    # startup()

    while True:
        query = takeCommand().lower()
        print(query)

        if "time" in query:
            time1()

        elif "date" in query:
            date()

        elif "cpu" in query:
            cpu()

        elif "screenshot" in query:
            screenshot()
            speak("Your screenshot has been taken.")

        elif "joke" in query:
            jokes()

        elif ("class" in query) or ("myclass" in query) or ("my class" in query):
            speak("Opening My class")
            myclass()

        elif "wikipedia" in query:
            speak("Searching...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(f'{query}', sentences=2)
            speak(result)
            print(result)

        elif "play songs" in query:
            songs_dir = "D:\Songs"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif "remember that" in query:
            speak("What should i remember?")
            data = takeCommand()
            speak("You said me to remember,"+data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif ("do you remember" in query) or ("do you remember anything" in query):
            remember = open("data.txt", "r")
            speak("you told me to remember that  " + remember.read())

        elif ("vlcplayer" in query) or ("player" in query) or ("video player" in query):
            speak("Opening VLC")
            os.system("VLC")

        elif ("offline" in query) or ("off" in query):
            speak("Bye and Have a great Day Sir, alex now going offline")
            print("Bye and Have a great Day Sir, alex now going offline")
            quit()

        elif ("logout" in query) or ("log out" in query):
            os.system("shutdown -l")

        elif "shutdown" in query:
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            os.system("shutdown /r /t 1")

        elif "weather in" in query:
            Temperature()

        elif "what is" in query or "who is" in query:
             question = query
             answer = computational_intelligence(question)
             speak(answer)

        elif "goodbye" in query or "offline" in query or "bye" in query:
            speak("Alright sir, going offline. It was nice working with you")
            sys.exit()
