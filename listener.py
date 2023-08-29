import speech_recognition as sr
import pyttsx3

def generate_audio(text):

    """
    Turns the passed text into speech and saves it to an audio file
    """

    engine = pyttsx3.init()

    # * Set the correct voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    
    # * Save the audio file to the frontend audio folder
    engine.save_to_file(text, 'audio/message.wav')

    # * Speak
    # engine.say(text)
    engine.runAndWait()
    engine.stop()


def listen(awake=False) -> dict:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        # print(audio)

    try:
        # text = recognizer.recognize_google(audio).lower()
        text = recognizer.recognize_google(audio).lower()
        print("You said:", text)
        
        response = {
            "message": text,
            "error": False
        }

        return response
    
    except sr.UnknownValueError as e:

        message = "The speech recognition software could not process what the user said \
                    Inform the user with a short message"
        # print("Sorry, I didn't catch that.")
        # speak("Sorry, I didn't catch that.")
        
        response = {
            "message": message,
            "error": True
        }
        
        return response
    
        
    except sr.RequestError as e:
        message = "There is an issue with the speech recognition service. \
                    Inform the user with a short message"
        # print("Sorry, there was an issue connecting to the speech recognition service.")
        # speak("Sorry, there was an issue connecting to the speech recognition service.")

        response = {
            "message": message,
            "error": True
        }

        return response


