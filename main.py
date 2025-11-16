
from time import time
import pyttsx3
import webbrowser
import speech_recognition as sr
import requests
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = os.environ.get("NEWS_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_MODELS_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"

def ask_github_model(prompt: str, model: str = "openai/gpt-4o"):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    resp = requests.post(API_URL, json=body, headers=headers)
    resp.raise_for_status()
    data = resp.json()    # data(dict) te id and choices(list of dict) thakbe
    return data["choices"][0]["message"]["content"]

def speak(text):
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    if "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://www.google.com")
    elif "open linkedin" in c.lower():
        speak("opening linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif "open facebook" in c.lower():
        speak("opening facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in c.lower():
        speak("opening instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open github" in c.lower():
        speak("opening github")
        webbrowser.open("https://www.github.com")
    elif "open gmail" in c.lower():
        speak("opening gmail")
        webbrowser.open("https://www.gmail.com")
    elif "news" in c.lower():
        speak("top news are")
        time.sleep(1)
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapikey}")

        if r.status_code == 200:
            data = r.json()
            articles = data["articles"]
            for article in articles:
                speak(article["title"]) 
                time.sleep(1)
    else:
       try:
            answer = ask_github_model(c)
            speak(answer)
       except Exception as e:
            print("Error calling GitHub Models API:", e)

if __name__ == "__main__":
    speak("initializing nafis...")

    while True:
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)
            print("You said: " + word)
            print()
            
            if word.lower() == "nafis":
                speak("yes")
                print("nafis activated")
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
