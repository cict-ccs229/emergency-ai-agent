import os
from dotenv import load_dotenv
from agent import root_agent

load_dotenv()  

def main():
    print("Roxas City Emergency Response Team - RCERT AI Assistant running.")
    while True:
        user_input = input("You: ")
        response = root_agent.chat(user_input)
        print("AI:", response.text)

if __name__ == "__main__":
    main()
