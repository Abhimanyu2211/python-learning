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
import re
import os
import re
import os
import webbrowser
import datetime
import wikipedia
import urllib.parse
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(message):
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()

def listen(timeout=8, phrase_time_limit=5):
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
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

def extract_song_name(command: str) -> str:
    """Try several patterns to extract the song name from the spoken command."""
    command = command.strip()
    patterns = [
        r"(?:play|play the|please play|could you play|play song|play music)\s+(?P<song>.+)",
        r"(?:music|song)\s+(?P<song>.+)",
        r"(?P<song>.+?)\s+on spotify",
    ]

    for pat in patterns:
        m = re.search(pat, command)
        if m:
            song = m.groupdict().get("song") or ""
            # strip common trailing words
            song = re.sub(r"\b(on spotify|on youtube|on youtube music)\b", "", song).strip()
            # remove polite words
            song = re.sub(r"\bplease|could you|would you\b", "", song).strip()
            return song

    # fallback: remove keywords and return remainder
    cleaned = re.sub(r"\b(play|play the|playlist|song|music|spotify)\b", "", command).strip()
    return cleaned

def open_spotify_search(song: str):
    if not song:
        return False
    query = urllib.parse.quote_plus(song)
    url = f"https://open.spotify.com/search/{query}"
    webbrowser.open_new_tab(url)
    return True

def is_exit_command(command: str) -> bool:
    """Return True if command is a request to exit/shutdown/quit/stop/goodbye."""
    return bool(re.search(r"\b(exit|shutdown|quit|stop|goodbye|bye)\b", command))

def understand_and_respond(command):
    if command == "":
        return True

    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")
        return True

    if "date" in command:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")
        return True

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return True

    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return True

    if "open spotify" in command and "search" not in command:
        speak("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
        return True

    if "wikipedia" in command:
        try:
            speak("Searching Wikipedia")
            topic = command.replace("wikipedia", "")
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except Exception:
            speak("Could not find information.")
        return True

    # music / play handling
    if any(k in command for k in ("play", "music", "song")):
        song = extract_song_name(command)

        if not song:
            # ask for the song and listen once
            speak("Which song do you want me to play?")
            follow = listen(timeout=6, phrase_time_limit=6)
            song = extract_song_name(follow)

        if not song:
            speak("I didn't catch the song name. Please try again.")
            return True

        speak(f"Searching Spotify for {song}")
        opened = open_spotify_search(song)
        if not opened:
            speak("Sorry, I couldn't open Spotify.")
        return True

    if is_exit_command(command):
        speak("Okay, shutting down. Goodbye.")
        return False

    speak("I heard you, but I am still learning.")
    return True

def start_assistant():
    speak("Hello, I am online and ready to help.")

    running = True
    while running:
        command = listen()
        # protect against None or non-string
        if command is None:
            command = ""
        running = understand_and_respond(command)

if __name__ == "__main__":
    start_assistant()
