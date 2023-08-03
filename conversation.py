class Conversation:
    def __init__(self, prompt=""):
        
        self.messages = [
            {
                "role": "system",
                "content": prompt
            }
        ]
    
    def add_message(self, role, content, function_name=""):
        """
        * Add a new message to the conversation

        * :param role (string): Set the role of the message. Options: "system", "assistant", "users"
        * :param message (string): Set the content of the message.
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
    
    def get_messages(self):
        return self.messages
