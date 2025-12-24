import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(message):
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
            return ""

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Network error.")
        return ""

def understand_and_respond(command):
    if command == "":
        return True

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")

    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open spotify" in command:
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")

    elif "wikipedia" in command:
        try:
            speak("Searching Wikipedia")
            topic = command.replace("wikipedia", "")
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak("Could not find information.")

    elif "play song" in command or "play music" in command:
        song = command.replace("play song", "").replace("play music", "").strip()

        if song == "":
            speak("Please tell me the song name.")
        else:
            speak(f"Playing {song} on Spotify")
            song = song.replace(" ", "%20")
            url = f"https://open.spotify.com/search/{song}"
            webbrowser.open(url)

    elif "exit" in command or "shutdown" in command:
        speak("Okay, shutting down. Goodbye.")
        return False

    else:
        speak("I heard you, but I am still learning.")

    return True

def start_assistant():
    speak("Hello, I am online and ready to help.")

    running = True
    while running:
        command = listen()
        running = understand_and_respond(command)

if __name__ == "__main__":
    start_assistant()
