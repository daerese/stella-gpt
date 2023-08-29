
"""
This class stores the messages sent between the user and 
ChatGPT to help rememeber the context of the conversation.
"""
from typing import List, Dict

class Conversation:
    def __init__(self, prompt: str =""):
        
        self.messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]
        self.is_awake = False
    
    def add_message(self, role: str, content: str, function_name: str =""):
        """
        Add a new message to the conversation

        Parameters:
        - role : str
            - The role of the the message. Options are: "user", "assistant", "function", and "system".
        - content : str
            - The contents of the message to be added to the conversation.
        - function_name : str (optional)
            - The name of the function if there is a function that needs to be called.
        """

        if (role == "function"):
            message = {
                "role": "function",
                "name": function_name,
                "content": content
            }
        else:
            message = {
                "role": role,
                "content": content
            }

        self.messages.append(message)
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        Returns a list of the messages in the current conversation.
        """
        return self.messages
