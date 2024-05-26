'''
python3 chat.py path/to/your/OPENAI_API_KEY.txt
'''
import os
import sys
import time
import openai
import tkinter as tk
from tkinter import scrolledtext, filedialog


# Init
OPENAI_API_KEY_PATH = sys.argv[1]
MODEL_NAME = 'gpt-3.5-turbo'
start_context = [
            {'role':'system',
            'content':'You are a helpful AI assistant'}
            ]


if os.path.exists(OPENAI_API_KEY_PATH):
    with open(OPENAI_API_KEY_PATH) as f:
        OPENAI_API_KEY = f.read().strip()
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        openai.api_key = OPENAI_API_KEY
else:
    print(OPENAI_API_KEY_PATH, ' NOT EXIST!')
    exit(-1)


def get_completion(prompt, model=MODEL_NAME, temperature=0):
    # generate message
    messages = [{'role':'user',
                 'content':prompt}
               ]
    # receive the response
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature # this is the degree of randomness of model
    )
    return response.choices[0].message['content']

def get_completion_from_messages(messages,model=MODEL_NAME, temperature=0):
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = temperature # this is the degree of randomness of model
    )
    return response.choices[0].message['content']

def collect_messages(context, user_message):
    # Append user message
    context.append({'role':'user','content':f"{user_message}"})
    # Send API
    response = get_completion_from_messages(context)
    # Append model output
    context.append({'role':'user','content':f"{user_message}"})
    return response


class ChatBot:

    def __init__(self, root):

        # Init
        self.root = root
        self.root.title("ChatGPT")
        self.font = ("Arial", 12)

        # Create a frame for the scrolled text area (chat display)
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(padx=10, pady=10)

        # Create the scrolled text widget for displaying messages
        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD,
                                                         state='disabled',
                                                         width=50,
                                                         height=20,
                                                         font=self.font)
        self.chat_display.pack()

        # Create a frame for the entry box and send button
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(padx=10, pady=10)

        # Create the entry box for typing messages
        self.message_entry = tk.Entry(self.entry_frame, width=40, font=self.font)
        self.message_entry.pack(side=tk.LEFT, padx=5)

        # Create the send button
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message,font=self.font)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Create the clear button
        self.clear_button = tk.Button(self.entry_frame, text="Reset", command=self.clear_chat,font=self.font)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Create the export button
        self.export_button = tk.Button(self.entry_frame, text="Export", command=self.export_chat,font=self.font)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # Bind the Return key to send message
        self.root.bind('<Return>', self.send_message)

        # Chat context
        self.context = start_context.copy()

    def send_message(self, event=None):
        # Get the message from the entry box
        user_message = self.message_entry.get()
        
        # Check if the message is not empty
        if user_message.strip():

            # Send API            
            msg = f"You: {user_message}\nChatGPT: {collect_messages(self.context, user_message)}\n"

            # Display the message in the chat display
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, msg)
            self.chat_display.config(state='disabled')
            self.chat_display.yview(tk.END)  # Scroll to the end

            # Clear the entry box
            self.message_entry.delete(0, tk.END)

    def clear_chat(self):
        
        # Reset context
        self.context = start_context.copy()

        # Clear the chat display
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0', tk.END)
        self.chat_display.config(state='disabled')

    def export_chat(self):
        # Ask the user for a file to save the chat conversation
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            # Export the chat display contents to the file
            with open(file_path, 'w') as file:
                self.chat_display.config(state='normal')
                file.write(self.chat_display.get('1.0', tk.END))
                self.chat_display.config(state='disabled')

if __name__ == "__main__":
    
    root = tk.Tk()
    app = ChatBot(root)
    root.mainloop()