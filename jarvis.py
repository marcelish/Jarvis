import pyttsx3
import speech_recognition as sr
import datetime
import os
from requests import get
import wikipedia
import sys
import random
import json
import pyautogui
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)
# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
# Function to take command from user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=8)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query
# to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good Morning!")
        speak(f"Currently it is {datetime.datetime.now().strftime('%I:%M %p')}")
    elif hour > 12 and hour < 18:
        speak("Good Afternoon!")
        speak(f"Currently it is {datetime.datetime.now().strftime('%I:%M %p')}")
    else:
        speak("Good Evening!")
        speak(f"Currently it is {datetime.datetime.now().strftime('%I:%M %p')}")
    speak("I am Jarvis. How may I help you?")
# to open any application
def open_application(query):
    # load the JSON file
    with open('open_applications.json', 'r') as file:
        apps = json.load(file)

    for app, path in apps.items():
        if f"open {app}" in query:
            speak(f"Opening {app.capitalize()}")
            if path.endswith('.lnk'):
                os.startfile(path)
            else:
                os.system(f"start {path}")
            return True
    return False
#to close any application
def close_application(query):
    # load the JSON file
    with open('close_applications.json', 'r') as file:
        applications = json.load(file)
    for app, process in applications.items():
        if f"close {app}" in query:
            speak(f"Closing {app.capitalize()}")
            os.system(f"taskkill /f /im {process}")
            return True
    return False
# to prompt for additional assistance
def additional_assistance_prompt():
    i = random.randint(0, 10)
    # load the JSON file
    with open('additional_assistance_prompts.json', 'r') as file:
        prompts = json.load(file)
    speak(prompts[i])
# to search on google or youtube
def search(query, url):
    speak(f"What do you want to search on {query}?")
    search = takeCommand().lower()
    url = f"{url}{search}"
    url = url.replace(" ", "+")
    os.system(f"start chrome {url}")
# to open wikipedia
def open_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    speak(results)
# to set an alarm
def set_alarm():
    speak("At what time should I set the alarm?")
    alarm_time = input("Enter the time in 24-hour format (HH:MM): ")
    return alarm_time
# check the alarm
def check_alarm(alarm_time, alarm):
    time = datetime.datetime.now().strftime("%H:%M")
    if time == alarm_time:
        speak("Wake up! It's time!")
        alarm = False
        return alarm
    return alarm
# main function to execute tasks
if __name__ == "__main__":
    alarm = False
    wish()
    while True:
        query = takeCommand().lower()
        # if i say jarvis then it will start listening
        if "jarvis" in query:
            speak("Yes sir")
            if "open youtube" in query:
                search("YouTube", "https://www.youtube.com/results?search_query=")
            elif "open google" in query:
                search("Google", "https://www.google.com/search?q=")
            elif "wikipedia" in query:
                open_wikipedia(query)   
            elif "open" in query:
                if open_application(query):
                    continue
                else:
                    speak("I'm sorry, I couldn't find the application you mentioned.")
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"Your IP Address is {ip}")
            elif "the time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
            # set an alarm
            elif "set an alarm" in query:
                alarm_time = set_alarm()
                alarm = True
            elif "switch window" in query:
                pyautogui.hotkey('alt', 'tab')
            elif "turn off the computer" in query:
                speak("Turning off the computer")
                os.system("shutdown /s /t 1")
            elif "restart the computer" in query:
                speak("Restarting the computer")
                os.system("shutdown /r /t 1")
            elif "sleep the computer" in query:
                speak("Sleeping the computer")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif "close" in query:
                if close_application(query):
                    continue
                else:
                    speak("I'm sorry, I couldn't find the application you mentioned.")
            # exit the program
            elif "no thanks" in query:
                speak("Thank you for using me. Have a good day!")
                sys.exit()
            # prompt for additional assistance
            additional_assistance_prompt()
        if "no thanks" in query:
                speak("Thank you for using me. Have a good day!")
                sys.exit()
        if alarm == True:
            check_alarm(alarm_time, alarm)