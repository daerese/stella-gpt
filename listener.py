import speech_recognition as sr
import pyttsx3

def speak(text):

    engine = pyttsx3.init()

    # * Set the correct voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
    # * Speak
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    

def listen():
    recognizer = sr.Recognizer()


    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)        

    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)
        return text
    except sr.UnknownValueError as e:
        print("Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that.")
        return e
    except sr.RequestError as e:
        print("Sorry, there was an issue connecting to the speech recognition service.")
        speak("Sorry, there was an issue connecting to the speech recognition service.")
        return e  
