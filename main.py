
import pyttsx3
import webbrowser
import speech_recognition as sr

recognizer = sr.Recognizer()
engine = pyttsx3.init()

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
    else:
        speak("command not recognized")

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
