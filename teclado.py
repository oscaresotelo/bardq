from Bard import Chatbot

import warnings
import sys

# Paste your Bard Token (check README.md for where to find yours) 
token = "Wghlci3JMlUaLO4_VZgMKjCDDhUSMRvL4049frEMZZaj3PK1cJ6iMDTJbZoeClmdcGaRYg."
# Initialize Google Bard API
chatbot = Chatbot(token)


def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']



def main():
   
    while True:
        try:
            # Get user input
            prompt_text = input("Enter your prompt: ")
            # If prompt is empty, start again
            if len(prompt_text.strip()) == 0:
                print("Empty prompt. Please enter again.")
                continue
            # Prompt Bard
            response = prompt_bard(prompt_text)
            print('Bard\'s response:', response)
            
        except KeyboardInterrupt:
            # Exit program on keyboard interrupt (Ctrl+C)
            print("\nExiting...")
            break

main()
