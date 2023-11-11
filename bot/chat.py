from twilio.rest import Client
from fastapi import FastAPI, Request, Form
from bot import chat_stuff
import uvicorn
from datetime import date

app = FastAPI()

account_sid = 'ACff85088079cdcfcc13db683ac7b628ec'
auth_token = '16aee1ffb3bd18efb38b8c08f4053db1'
client = Client(account_sid, auth_token)

"""
message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='Your appointment is coming up on July 21 at 3PM',
  to='whatsapp:+237656047446'
)
"""

# this function sends a <message> to <contact_phone>
def send_reply(contact_phone: str, message: str) -> None:
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:{contact_phone}'
    )

d1=date.today()
today=d1.strftime("%d/%m/%Y")
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
@app.get("/")
async def index():
    return "hello"

@app.post("/message")
async def handle_message(req: Request, Body: str = Form()):


    
    form_data = await req.form()
    print("Got message", Body)
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]

    messages.append({ "role": "user", "content":  Body })

    chatgpt_reply = chat_stuff(messages)
    messages.append({ "role": "assistant", "content": chatgpt_reply })
    send_reply(whatsapp_number, chatgpt_reply)

    return "You got something my friend"

uvicorn.run(host="0.0.0.0", app=app)


'''
@app.post("/message")
async def reply(request: Request, Body: str = Form(), db: Session = Depends(get_db)):
    
    form_data = await request.form()
    whatsapp_number = form_data['From'].split("whatsapp:")[-1]
    print(f"Sending the ChatGPT response to this number: {whatsapp_number}")

    last_conversations = db.query(Conversation).filter_by(sender=whatsapp_number).order_by(Conversation.id.desc()).limit(10).all()

    last_conversations = last_conversations[::-1]

    d1=date.today()
    today=d1.strftime("%d/%m/%Y")
    messages=[{"role": "system", "content": """You are a shop assitant chatbot and your job is to do the following:\n
               1. Ask for gmail to use and send a reminder.\n 
               2. Don't ask for phone number.\n 
               3. At the end of the conversation when youre sure youve collected ALL the information including the email for reminder before you say something almost excactly like this:("Great! You are booked for a [SERVICE] appointment on [DATE] at [TIME]. Please arrive 10 minutes prior to your appointment time. We'll create a reminder for [EMAIL] so you dont forget).\n
               4. Let the date be in the form dd/mm/yy wehre dd is the day num ,mm is the month num and yy is the year num and also the time in the form hh:mm where hh is the hour and mm is the minute in french format
               5. Dont answer any questions that doesnt concern barbing
               6.The barbershop is located at sml madagascar
               7.it has the following services:
                * Freestyle for 5000 frs
                * normal haircut for 2000 frs
                ^ haircut with black color 3000frs
                ^ haircut with color 5000 for yellow, 10000 or 15000 for any other color
               
               """},
              
              {"role": "system", "content": "The date of today is {} i am using this so that if a client says tomorrow i can add 1day if a client says next week i can add 7 days and so on".format(today)}
              ]

    for conversation in last_conversations:
        messages.append({"role": "user", "content": conversation.message})
        messages.append({"role": "system", "content": conversation.response})
    messages.append({"role":"user","content":Body})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5
        )

    chatgpt_response = response.choices[0].message.content

    try:
        messages.append({"role": "system", "content": chatgpt_response})
        conversation = Conversation(
            sender=whatsapp_number,
            message=Body,
            response=chatgpt_response
            )
        db.add(conversation)
        db.commit()
        logger.info(f"Conversation #{conversation.id} stored in database")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error storing conversation in database: {e}")
    
    send_message(whatsapp_number, chatgpt_response)
    
    #check if its the final message
    if check_for_end(chatgpt_response)=="1":
        something=final_extract(chatgpt_response)
        print(something)
        dateTime1=dateTime(something[1],something[2])
        create('Barber Appointment',something[0],dateTime1,dateTime1,something[3]+".com")
        
    #if it is the final message create event
    return ""'

'''

'''
# Standard library import
import logging

# Third-party imports
from twilio.rest import Client
from decouple import config


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = config("TWILIO_ACCOUNT_SID")
auth_token = config("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)
twilio_number = config('TWILIO_NUMBER')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
            )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

    '''