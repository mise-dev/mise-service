from openai import OpenAI
from decouple import config
from datetime import date
from extract import check_for_end

d1=date.today()
today=d1.strftime("%d/%m/%Y")
client = OpenAI(api_key="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")

# lets say all the info a seller needs to collect from a certain client
# Product information to consider
# - Name str
# - Variant str 
# - Shipping adddress str


messages=[{"role": "system", "content": """You are a shop assistant chatbot and your job is to do the following:\n
 1. Provide product information after the client has told you what they want (name, variants, prices, descriptions,)
 2. Collect all the information that you think will be useful to collect from a client trying to buy a certain product.\n
 3. At the end of the conversation when youre sure youve collected ALL the information say something almost excactly like this:("Great! You have purchased a [product name],[Size an COLOR or whatever varriant],for [price], on the [Date] 🛍
).\n
 4. Let the date be in the form DD/MM/YY wehre DD is the day num ,MM is the month num and YY is the year num and also the time in the form hh:mm where hh is the hour and mm is the minute
 5. Dont answer any questions that doesnt concern shopping 
 """},

{"role": "system", "content": "The date of today is {} i am using this so that if a client says something like tomorrow you can calculate the date by knowing todays date".format(today)}
]

def chat_stuff( messages: list):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
    )

    chatgpt_response = response.choices[0].message.content
  # print("ChatGPT: {}".format(chatgpt_response))
  # user_input = input("You: ")#autocompleted prompt
  
  # has to be written in chat.py
  # messages.append({"role": "user", "content": message}) #autocompleted
    # messages.append({"role": "assistant", "content": chatgpt_response})#autocompleted
  # if check_for_end(chatgpt_response) or '🛍' in chatgpt_response:
    return chatgpt_response
  
"""
conversation_ended = False
while "Josias" != "the goat":
  conversation_ended = False 

  response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
  )
  chatgpt_response = response.choices[0].message.content
  print("ChatGPT: {}".format(chatgpt_response))
  user_input = input("You: ")#autocompleted prompt
  if user_input == "q": 
    quit()
  messages.append({"role": "user", "content": user_input}) #autocompleted
  messages.append({"role": "assistant", "content": chatgpt_response})#autocompleted
  # if check_for_end(chatgpt_response) or '🛍' in chatgpt_response:
  if '🛍' in chatgpt_response:
    conversation_ended = True
    break
# print("ChatGPT: {}".format(chatgpt_response))
"""