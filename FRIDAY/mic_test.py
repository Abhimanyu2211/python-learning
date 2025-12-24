import os
import time
import speech_recognition as sr

# Use Homebrew FLAC on macOS
os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin"

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.6
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.4

with sr.Microphone() as source:
    print("Listening... Speak clearly.")
    recognizer.adjust_for_ambient_noise(source, duration=0.3)

    try:
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
    except sr.WaitTimeoutError:
        print("No speech detected.")
        exit()

print("Recognizing speech...")

start_time = time.time()

try:
    text = recognizer.recognize_google(audio, language="en-IN")
    print("You said:", text)
    print("Time taken:", round(time.time() - start_time, 2), "seconds")

except sr.UnknownValueError:
    print("Sorry, I could not understand what you said. Please speak clearly.")
except sr.RequestError:
    print("Network error. Please check your internet connection.")
