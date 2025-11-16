import time
import pyttsx3
import webbrowser
import speech_recognition as sr
import requests
import os
from sites_Library import sites
from playable_Library import playables

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = os.environ.get("NEWS_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_MODELS_TOKEN")
API_URL = "https://models.github.ai/inference/chat/completions"
recognition_enabled = True

# Try to import the optional OpenAI client (client.py). If present and configured,
# prefer it for conversational queries. Import safely so main.py still runs without it.
try:
    from client import has_api_key as openai_has_key, get_response as openai_get_response
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


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
    global recognition_enabled
    recognition_enabled = False
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

    time.sleep(0.5)
    recognition_enabled = True


def processCommand(c):
    if c.lower().startswith("open"):
        site_name = c.lower().split(" ")[1]
        webbrowser.open(sites.get(site_name))
    
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
    
    elif "play" in c.lower():
        play_item = c.lower().split(" ")[1]
        webbrowser.open(playables.get(play_item))

    else:
       try:
            # Prefer local OpenAI client when available and configured, otherwise use GitHub Models
            if OPENAI_AVAILABLE and openai_has_key():
                answer = openai_get_response(c)
            else:
                answer = ask_github_model(c)
            speak(answer)
       except Exception as e:
            print("Error calling model API:", e)


def main():
    speak("initializing Nexus...")

    while True:
        if not recognition_enabled:
            continue

        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)
            print("You said: " + word)
            print()
            
            if word.lower() == "nexus":
                speak("yes")
                print("nexus activated")
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    if command.lower() in ("exit", "quit", "deactivate"):
                        speak("deactivating nexus.")
                        break
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))


if __name__ == "__main__":
    main()