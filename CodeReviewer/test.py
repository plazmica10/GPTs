import openai
from dotenv import dotenv_values
import argparse

config = dotenv_values("../.env")
openai.api_key = config["AIKEY"]

#functions that color the text
def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end

def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end

def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end

def main():
    #Command line argument for personality of the chatbot
    parser = argparse.ArgumentParser(description="Command line chatbot")
    parser.add_argument("--personality", type=str,help="A brief summary of the chatbot's personality", default="friendly and helpful chatbot")
    args = parser.parse_args()

    initial_prompt = f"You are a conversational chatbot. Your pesonality is: {args.personality}" #system message for overall directions 
    messages = [{"role": "system","content": initial_prompt}] #list of messages so that the chatbot can keep track of the conversation

    while True: #loop to keep asking for input
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})#adding user input to the list of messages

            #Comlpetion request to the OpenAI API
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",#can replace with gtp-4
                messages=messages,
                stream=True
            )

            response=""
            print(bold(red("Assistant: ")), end="")
            #openai sends generator and it needs to be iterated through, because of stream=True
            for data in res:
                if "content" in data.choices[0].delta:
                    response += (data.choices[0].delta.content)
                    print(data.choices[0].delta.content, end="", flush=True)
            print("")
            messages.append({"role": "assistant", "content": response})
            
            # HANDLING MESSAGES AND PRINTING WITHOUT STREAM
            # messages.append(res["choices"][0]["message"].to_dict())  #add the chatbot's response to the list of messages and convert it to a dictionary because chatbot's response is a class object
            # print(bold(red("Assistant: ")),res["choices"][0]["message"]["content"])
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()