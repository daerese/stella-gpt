
import elevenlabs as eleven
import openai
import json
import eel
import os

from typing import Dict, Any
from dotenv import load_dotenv

# * Custom python files
from commands import *
from commands_as_json import commands
from spotify_player import Spotify_Player   
from conversation import Conversation
from tts import generate_audio

# *******************************
# * Environment variables
load_dotenv('.env')

# * Set the following variables in your .env file.
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY")

# * Setting the API Keys
openai.api_key = OPENAI_API_KEY
eleven.set_api_key(ELEVENLABS_API_KEY if ELEVENLABS_API_KEY else "")

# *******************************
# * Utility functions
def extract_args(args: dict) -> list:
    """
    Extracts the arguments from ChatGPT's response when
    it wants to call a function.
    """
    args_to_call = []
    for arg in args: 
        args_to_call.append(args.get(arg))
    
    return args_to_call

# *******************************
# * ElevenLabs Voice Setup

def get_voices():
    """
    Use this to view the list of voices that can be used
    for text-to-speech.
    """
    return eleven.voices()  


# * The following Voice ID is for my preferred voice --> Caroline
# * You can view all the voices available to you with this link, 
# * then set the ID of the voice you want:
# https://api.elevenlabs.io/docs#/voices/Get_voices_v1_voices_get
VOICE_ID : str = "XrExE9yKIg1WjnnlVkGX"

try:
    voices = get_voices()

    main_voice = list(filter(lambda voice: voice.voice_id == VOICE_ID, voices))

    # * If my voice isn't available to you, then a default voice is selected.
    if len(main_voice) > 0:
        main_voice = main_voice[0]
    else:
        main_voice = list(filter(lambda voice: voice.name.lower() == "matilda", voices))[0]
except:
    main_voice = None
# *******************************

available_commands = {}

for command in commands:

    # * eval() converts a string type into a function
    command_name = command["name"]
    available_commands[command_name] = eval(command_name)


# * ChatGPT Prompt configuration
prompt = """
            - Your name is Stella. You are both my assistant, and my friend. You often like to be sarcastic, and occasionally make jokes.
            - You are connected to an application on my computer. I'm using my voice to communicate with you, and turning my speech into text via a speech recognition software.
            - Keep your responses concise, breif, and not too long. Your responses should not exceed 100 tokens.
            - I may ask for a task related to taking an action on my computer, such as opening an application, or sending an email.
            - Do not deny the request or say that you can't do it unless it's absolutely impossible.
            - You have the ability to play something on Spotify on the user's computer if you are asked.
            - Using the ChatGPT API, I will pass functions to you that allow you to execute these commands.
            - Finally, I will also pass a function to you called sleep().
              If the user doesn't need any more assistance at the moment, or if you presume they are finished speaking to you for now,
              then make sure to call the sleep function.
        """

conversation = Conversation(prompt)



@eel.expose
def generate_gpt_response(text: str) -> Dict[str, Any]:

    """
    This recieves a text input, and sends it to ChatGPT. A response
    from ChatGPT is then created, and audio will be generated from that response

    Parameters:
    - text : str 
        - The text input to be sent to ChatGPT
    
    Returns:
    - json object: An object with a status code indicating the 
    success or failure of generating a response.
    """

    # * If not awake, check if the user said the awake command "Hey stella"
    
    conversation.add_message(role="user", content=text)

    # * A personal status code to indicate to my Javascript 
    # * whether the 
    status = {
        "status": 200,
        "statusMessage": "",
        "gptMessage": "",
        "go_to_sleep": False
    }

    try:
        # * Send the message to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation.get_messages(),

            functions=commands,
            function_call="auto",

            temperature=1.25,
            max_tokens=120,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except:
        status["status"] = 500
        status["statusMessage"] = "There was a ChatGPT response error. Check your ChatGPT API usage at: \nhttps://platform.openai.com/account/usage"
        return json.dumps(status)
    else:
        # * Append ChatGPT response to have context in the current conversation.
        message = response["choices"][0]["message"]
        # print(message)
        # * Function calling
        if message.get("function_call"):

            # * Extract the information about the function that 
            # * ChatGPT wants to be called.
            function_name = message["function_call"]["name"]
            arguments = json.loads(message["function_call"]["arguments"])

            function_to_call = available_commands[function_name]

            # * Call the function, using the arguments. 
            # * Also, determine if the use_spotify_player function is being called

            if function_name == "use_spotify_player":

                # * Create a spotify object if it isn't already created.
                if "spotify_object" not in locals():
                    spotify_object = Spotify_Player()

                # * Check if the user has their Spotify API info set up.
                if spotify_object.check_for_client_id():
                    function_response = function_to_call(spotify_object, *extract_args(arguments))
                else:
                    function_response = "Spotify_Player is unavailable"


            elif function_name == "sleep":
                status["go_to_sleep"] = True
                function_response = function_to_call()
            else:
                function_response = function_to_call(*extract_args(arguments))

            conversation.add_message(role="function", 
                                    content=function_response,
                                    function_name=function_name,
                                    )
            
            # * Generate another response based on the called function
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation.get_messages(),

                temperature=1.25,
                max_tokens=75,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            message = second_response["choices"][0]["message"]

        conversation.add_message(content=message["content"], role="assistant")
        print(message["content"])

        # * Generate audio from ChatGPT's response
        if main_voice:
            try:
                # * Generating the audio using eleven labs
                audio = eleven.generate(
                                text=message["content"],
                                voice=main_voice,
                                model="eleven_multilingual_v1"
                            )
                
                eleven.save(audio, "audio/message.wav")
            except:
                # * Using built in tts if elevenlabs doesn't work or isn't set up.
                print("Eleven labs error")
                generate_audio(message["content"])
        else:
            generate_audio(message["content"])


        # * Get the message to the frontend.
        status["gptMessage"] = message["content"]
        status["statusMessage"] = "Success"

        return json.dumps(status)

# *##########################################

def main():
    
    eel.init('gui')

    eel.start('main.html')

if __name__ == '__main__':
    main()