import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import urllib.parse
import re
import os
import sys
import time

#  FRIDAY voice assistant 
# This file keeps the original behaviour but uses clearer, human-friendly comments
# and tidy imports. It opens Google, searches Wikipedia, opens news, and opens
# Spotify search results for a spoken song name.

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(message: str) -> None:
    """Speak a short message and print it to the console for visibility."""
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()


def listen(timeout: int = 8, phrase_time_limit: int = 5) -> str:
    """Listen once from the default microphone and return recognized text.

    Returns an empty string if nothing useful was heard or recognition failed.
    """
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        # sample ambient noise briefly — shorter duration keeps responsiveness.
        # If your environment is noisy, increase this a bit, otherwise keep ~0.8s.
        r.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
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
    """Try to extract a song title (optionally with artist) from the phrase.

    Examples it handles:
    - "play shape of you"
    - "shape of you on spotify"
    - "play the song shape of you"
    Returns an empty string when nothing looks like a title.
    """
    if not command:
        return ""

    patterns = [
        r"(?:play|play song|play music|song|music)\s+(?P<song>.+)",
        r"(?P<song>.+?)\s+on spotify",
    ]

    for pat in patterns:
        m = re.search(pat, command, flags=re.I)
        if m:
            return m.group("song").strip()

    # Fallback: remove common keywords and return the rest
    cleaned = re.sub(r"\b(play|play the|song|music|spotify)\b", "", command, flags=re.I).strip()
    return cleaned


def open_spotify_search(song: str) -> None:
    """Open Spotify's web search page for the given song string."""
    if not song:
        return
    query = urllib.parse.quote_plus(song)
    url = f"https://open.spotify.com/search/{query}"
    webbrowser.open_new_tab(url)


def search_wikipedia(topic: str) -> None:
    """Try to read a short Wikipedia summary; fall back to a web search if needed."""
    if not topic:
        return
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except Exception:
        speak("I could not find this topic on Wikipedia; opening web results.")
        webbrowser.open_new_tab(f"https://www.google.com/search?q={urllib.parse.quote_plus(topic)}")


def open_news(topic: str) -> None:
    """Open Google News search results for the topic."""
    if not topic:
        return
    url = f"https://news.google.com/search?q={urllib.parse.quote_plus(topic)}"
    webbrowser.open_new_tab(url)
    speak(f"Showing news about {topic}")


def confirm_action(prompt: str, timeout: int = 4) -> bool:
    """Ask a yes/no question and return True for yes-like answers.

    This helps avoid accidental actions triggered by brief background noise.
    """
    speak(prompt)
    # listen briefly for a confirmation to stay responsive
    reply = listen(timeout=timeout, phrase_time_limit=2)
    if not reply:
        return False
    # accept a few affirmative replies
    return bool(re.search(r"\b(yes|yeah|yep|sure|ok|okay|please do)\b", reply, flags=re.I))


def is_exit_command(command: str) -> bool:
    """Return True when the user asked the assistant to stop."""
    if not command:
        return False
    return bool(re.search(r"\b(exit|shutdown|quit|stop|bye|goodbye)\b", command, flags=re.I))


def understand_and_respond(command: str) -> bool:
    """Interpret the user's command and take an action.

    Returns False to stop the main loop, True to continue.
    """
    if not command:
        return True

    # Immediate exit handling: if the user asked to stop, say goodbye and quit.
    # We handle this first so other rules (like 'play' or 'search') don't interfere.
    if is_exit_command(command):
        speak("Okay, shutting down. Goodbye.")
        # small console hint and a short sleep to ensure audio finishes
        print("Exiting...")
        time.sleep(0.2)
        sys.exit(0)

    # time/date
    if re.search(r"\btime\b", command):
        speak(datetime.datetime.now().strftime("The time is %I:%M %p"))
        return True
    if re.search(r"\bdate\b", command):
        speak(datetime.datetime.now().strftime("Today's date is %d %B %Y"))
        return True

    # open google explicitly
    if re.search(r"\b(open|go to)\b.*\bgoogle\b", command):
        speak("Opening Google")
        webbrowser.open_new_tab("https://www.google.com")
        return True

    # search commands (prefer Wikipedia)
    m = re.search(r"\b(?:search|search for|search about|tell me about|what is|who is)\b\s*(?P<topic>.+)", command, flags=re.I)
    if m:
        topic = m.group("topic").strip()
        if re.search(r"\bnews\b", topic, flags=re.I) or re.search(r"\bnews\b", command, flags=re.I):
            # user asked for news
            t = re.sub(r"\b(latest|today|news|about|search for|search about)\b", "", topic, flags=re.I).strip()
            if not t:
                speak("What news should I search for?")
                t = listen()
            if t:
                open_news(t)
            return True

        if topic:
            speak(f"Searching Wikipedia for {topic}")
            search_wikipedia(topic)
        else:
            speak("What should I search for?")
        return True

    # open youtube / open spotify (explicit)
    if re.search(r"\bopen\b.*\byoutube\b", command, flags=re.I):
        speak("Opening YouTube")
        webbrowser.open_new_tab("https://www.youtube.com")
        return True
    if re.search(r"\bopen\b.*\bspotify\b", command, flags=re.I) and not re.search(r"\bplay\b", command, flags=re.I):
        speak("Opening Spotify")
        webbrowser.open_new_tab("https://open.spotify.com")
        return True

    # wikipedia mention without explicit 'search' phrasing
    if re.search(r"\bwikipedia\b", command, flags=re.I):
        topic = re.sub(r"\bwikipedia\b", "", command, flags=re.I).strip()
        if not topic:
            speak("What should I search on Wikipedia?")
            topic = listen()
        if topic:
            speak(f"Searching Wikipedia for {topic}")
            search_wikipedia(topic)
        return True

    # play music
    if re.search(r"\b(play|song|music)\b", command, flags=re.I):
        song = extract_song_name(command)
        if not song:
            speak("Which song do you want me to play?")
            follow = listen()
            if follow:
                song = extract_song_name(follow)
        if song:
            # remove leftover words like 'play' and be tolerant of extra words
            song = re.sub(r"\bplay\b", "", song, flags=re.I).strip()
            # open spotify search first so it appears immediately, then speak
            open_spotify_search(song)
            speak(f"Playing {song} on Spotify")
        return True

    # exit
    if is_exit_command(command):
        speak("Okay, shutting down. Goodbye.")
        return False

    speak("I heard you, but I am still learning.")
    return True


def start_assistant() -> None:
    """Start the assistant loop."""
    speak("Hello, I am online and ready to help.")
    running = True
    while running:
        command = listen()
        running = understand_and_respond(command)


if __name__ == "__main__":
    start_assistant()
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import urllib.parse
import re
import os
import wikipedia
import urllib.parse
import re
import os

# humanxie — friendly voice assistant (humanized comments)
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(message):
    # Speak and also print so you can see what's happening in the terminal
    print("Assistant:", message)
    engine.say(message)
    engine.runAndWait()

def listen(timeout=8, phrase_time_limit=5):
    # Listen once and return the recognized text (lowercased). Returns empty string on failure.
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
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
    return ""


# Spotify helpers — small utilities to find a song name in what you said
def extract_song_name(command):
    patterns = [
        r"(?:play|play song|play music|song|music)\s+(?P<song>.+)",
        r"(?P<song>.+?)\s+on spotify",
    ]

    for pat in patterns:
        match = re.search(pat, command)
        if match:
            return match.group("song").strip()

    cleaned = re.sub(r"\b(play|song|music|spotify)\b", "", command).strip()
    return cleaned

def open_spotify_search(song):
    query = urllib.parse.quote_plus(song)
    url = f"https://open.spotify.com/search/{query}"
    webbrowser.open_new_tab(url)

# Lookup helpers — Wikipedia and news
def search_wikipedia(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except Exception:
        speak("I could not find this topic on Wikipedia.")
        webbrowser.open_new_tab(
            f"https://www.google.com/search?q={urllib.parse.quote_plus(topic)}"
        )

def open_news(topic):
    url = f"https://news.google.com/search?q={urllib.parse.quote_plus(topic)}"
    webbrowser.open_new_tab(url)
    speak(f"Here are the latest news about {topic}")

def is_exit_command(command):
    return bool(re.search(r"\b(exit|shutdown|quit|stop|bye|goodbye)\b", command))

# Main command handling — interpret what the user said and act
def understand_and_respond(command):
    if not command:
        return True

    # time/date
    if "time" in command:
        speak(datetime.datetime.now().strftime("The time is %I:%M %p"))
        return True
    if "date" in command:
        speak(datetime.datetime.now().strftime("Today's date is %d %B %Y"))
        return True

    # explicit: open google
    if re.search(r"\bopen\b.*\bgoogle\b", command) or re.search(r"\bgo to google\b", command):
        speak("Opening Google")
        webbrowser.open_new_tab("https://www.google.com")
        return True

    # explicit: search <topic> or search about <topic> — prefer wikipedia
    m = re.search(r"\b(?:search|search for|search about|tell me about|what is|who is)\b\s*(?P<topic>.+)", command)
    if m:
        topic = m.group("topic").strip()
        # if user explicitly says 'news' or 'latest news about X', route to news
        if re.search(r"\bnews\b", topic) or "news" in command:
            # remove leading words
            t = re.sub(r"\b(latest|today|news|about|search for|search about)\b", "", topic).strip()
            if not t:
                speak("What news should I search for?")
                t = listen()
            if t:
                open_news(t)
            return True

        if topic:
            speak(f"Searching Wikipedia for {topic}")
            search_wikipedia(topic)
        else:
            speak("What should I search for?")
        return True

    # open youtube/spotify — require stricter matching and a quick confirmation
    if re.search(r"\b(open|go to|launch)\b.*\byoutube\b", command, flags=re.I):
        # ignore single-word noise
        if len(command.split()) < 2:
            return True
        if confirm_action("Do you want me to open YouTube?"):
            # open first so the browser appears immediately,
            # then announce the action (TTS may take a moment)
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening YouTube")
        else:
            speak("Okay, not opening YouTube.")
        return True

    if re.search(r"\b(open|go to|launch)\b.*\bspotify\b", command, flags=re.I) and not re.search(r"\bplay\b", command, flags=re.I):
        if len(command.split()) < 2:
            return True
        if confirm_action("Do you want me to open Spotify?"):
            webbrowser.open_new_tab("https://open.spotify.com")
            speak("Opening Spotify")
        else:
            speak("Okay, not opening Spotify.")
        return True

    # wikipedia direct mention without explicit search phrase
    if "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        if not topic:
            speak("What should I search on Wikipedia?")
            topic = listen()
        if topic:
            speak(f"Searching Wikipedia for {topic}")
            search_wikipedia(topic)
        return True

    # play music
    if any(word in command for word in ("play", "song", "music")):
        song = extract_song_name(command)
        if not song:
            speak("Which song do you want me to play?")
            follow = listen()
            if follow:
                # try to extract a song name from the follow-up
                song = extract_song_name(follow)
        # clean song (remove leading verbs like 'play')
        if song:
            song = re.sub(r"\bplay\b", "", song, flags=re.I).strip()
            speak(f"Playing {song} on Spotify")
            open_spotify_search(song)
        return True

    # exit
    if is_exit_command(command):
        speak("Okay, shutting down. Goodbye.")
        return False

    speak("I heard you, but I am still learning.")
    return True

def start_assistant():
    # Greet once, then keep listening until user asks to stop
    speak("Hello, I am online and ready to help.")
    running = True
    while running:
        command = listen()
        running = understand_and_respond(command)


if __name__ == "__main__":
    start_assistant()
