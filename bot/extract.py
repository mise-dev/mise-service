import cohere
from cohere.responses.classify import Example
import random
import datetime


co = cohere.Client('NE2jpuOVpPyOaFliU7Oz4yqqHLYiP9h8t5K0S32X')

def check_for_end(answer):
    examples1=[]
    appointment_messages = [
      "Great! We have taken note of your purchase. Please approve and we'll validate.",
      "You're welcome. We have taken note of your purchase",
      "Thank your for buying with us. We can't wait to see you again.",
      "Your product has shipped and will arrive in 3 days.",
    ]
    examples1 += [Example(message, "1") for message in appointment_messages]

#this has all the zeros
    example=[
                Example(" I'm sorry, but we are closed on Mondays. Our business hours are from Tuesday to Sunday, from 9:00 AM to 7:00 PM. Would you like to schedule an appointment for a different day?","0"),
                Example("That works for me. Can I get your name and phone number please?","0"),
                Example("Hello! How can I assist you today,","0"),
                Example("Hello! Is there anything else I can assist you with?","0"),
                Example(" Great! May I know your Gmail address so I can send you a reminder for your appointment?","0"),
                Example("I'm sorry, but Friday 16th June 2023 has already passed. Could you please provide a different date?","0"),
                Example(" I'm sorry, but our barbershop closes at 9 pm. Our last appointment is at 8 pm. Would you like to schedule your appointment for another time?","0"),
                Example("I'm sorry but it seems youve already made an appoinment for 17/06/23 at 5:00PM.Is there anything else i can help you with","0"),
                Example("Great just to comfirm you will lik eto book an appoinment for a burst fade tomorrow at 5pm","0"),
                Example("sorry i cannot do that","0"),

        ]


    for i in example:
        examples1.append(i)

    classifications = co.classify(
        model='embed-english-v2.0',
        inputs=[answer],
        examples=tuple(examples1)
    )

    print('The confidence levels of the labels are: {}'.format(
        classifications.classifications))

    predict= classifications.classifications[0].prediction

    return bool(int(predict if predict is not None else '0'))

class cohereExtractor():
    def __init__(self, examples, example_labels, labels, task_desciption, example_prompt):
        self.examples = examples
        self.example_labels = example_labels
        self.labels = labels
        self.task_desciption = task_desciption
        self.example_prompt = example_prompt

    def make_prompt(self, example):
        examples = self.examples + [example]
        labels = self.example_labels + [""]
        return (self.task_desciption +
                "\n---\n".join( [examples[i] + "\n" +
                                self.example_prompt + 
                                labels[i] for i in range(len(examples))]))

    def extract(self, example):
        extraction = co.generate(
            model='xlarge',
            prompt=self.make_prompt(example),
            max_tokens=10,
            temperature=0.1,
            stop_sequences=["\n"])
        return(extraction.generations[0].text[:-1])


def final_extract(text):

    time_examples = []
    date_examples=[]
    service_examples=[]
    email_examples=[]
    emails=["glenmue@gmail.com","loismueblshblahblah568@gmail.com","velocity@outlook.com","velocity2020@icloud.com","suckmadick@yahoo.com","imarpusay1000@outlook.com","somebodiesname@gmail.com","hello@gmail.com","ndjosiasaurel@gmail.com","samueletoo9@emial.com"]
    for i in range(10):
        date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))
        time = datetime.time(hour=random.randint(0, 23), minute=random.choice([0, 15, 30, 45]))

        haircut_type = random.choice(["buzz cut", "crew cut", "fade", "undercut"])
        email=emails[i][:-4]
        appointment_time = "{}".format(time.strftime('%I:%M'))
        appointment_date = date.strftime('%d/%m/%y')
        appointment_message = "Great! You are booked for a {} appointment on {} at {}. Please arrive 10 minutes prior to your appointment time. We'll create a reminder for {}.com so you dont forget.".format(haircut_type,appointment_date,appointment_time,email)
        time_examples.append((appointment_time, appointment_message))
        date_examples.append((appointment_date,appointment_message))
        service_examples.append((haircut_type,appointment_message))
        email_examples.append((email,appointment_message))

    cohereEmailExtractor = cohereExtractor([e[1] for e in email_examples], 
                                            [e[0] for e in email_examples], 
                                            [],
                                            "sup", 
                                            "extract email from text message")
    cohereTimeExtractor = cohereExtractor([e[1] for e in time_examples], 
                                            [e[0] for e in time_examples], 
                                            [],
                                            "sup", 
                                            "extract time from text message")
    cohereDateExtractor = cohereExtractor([e[1] for e in date_examples], 
                                            [e[0] for e in date_examples], 
                                            [],
                                            "sup", 
                                            "extract date from text message")
    cohereServiceExtractor = cohereExtractor([e[1] for e in service_examples], 
                                            [e[0] for e in service_examples], 
                                            [],
                                            "sup", 
                                            "extract service from text message")


    return [cohereServiceExtractor.extract(text),cohereDateExtractor.extract(text),cohereTimeExtractor.extract(text),cohereEmailExtractor.extract(text)]

# text = "Hi John! Just wanted to confirm your appointment for Friday at 1 PM. Please let me know if you need to reschedule or cancel. Thanks!"
# print("SERVICE: {}\t DATE: {}\t TIME: {}\n".format(cohereServiceExtractor.extract(text),cohereDateExtractor.extract(text),cohereTimeExtractor.extract(text)))
# while True:
#     text=input("\nGLEN:")
#     if check_for_end(text)=="1":
#         print("SERVICE: {}\t DATE: {}\t TIME: {}\n Email:{}".format(cohereServiceExtractor.extract(text),cohereDateExtractor.extract(text),cohereTimeExtractor.extract(text),cohereEmailExtractor.extract(text)))
#     else:
#         print("nope\n")


#####################################################################################################

##########################################################################################
# # import spacy and load a small English model
# import spacy



# text = """            message            |                                                                                                 response      
#             ----+---------------+-------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#             | I need a cut tomorrow| Sure, what type of haircut would you like?
#             | Haircut                       | Sure, when would you like to schedule your haircut, Glen?
#             | Today                         | I'm sorry, but our schedule is full for today. Would you like to schedule your haircut for tomorrow?                                             
#             | 5PM tomorrow                  | Great, we have an opening at 5 PM tomorrow. Can I have your phone number to confirm the appointment, Glen?
#             | 673594931                     | Thank you, Glen. Your appointment for a haircut is confirmed for tomorrow at 5 PM. We will send you a reminder message on your phone number 673594931. Do you have any special requests for your haircut?
#             | Hair dye                      | Sure, what color would you like to dye your hair, Glen?
#             | black                          | Alright, we offer multiple shades of black, would you like a light, medium or dark gold color?
#             | dark                         | Sounds good! We will make sure to have the dark black hair dye ready for your appointment tomorrow at 5 PM, Glen. Is there anything else you would like to add or ask about your appointment?
#             | No                            | Alright then, thank you for scheduling your appointment with us, Glen. We will see you tomorrow at 5 PM for your haircut and dark black hair dye. Have a great day!
#             (9 rows)"""


# def extract_appointment_details(text):
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)
#     info = ["name", "phone number", "date", "time", "service", "color"]
#     data = {}
#     for ent in doc.ents:
#         if ent.label_ == "PERSON" and info[0] not in data:
#             data[info[0]] = ent.text
#         elif ent.label_ == "CARDINAL" and info[1] not in data:
#             data[info[1]] = ent.text
#         elif ent.label_ == "DATE" and info[2] not in data:
#             data[info[2]] = ent.text
#         elif ent.label_ == "TIME" and info[3] not in data:
#             data[info[3]] = ent.text
#     for chunk in doc.noun_chunks:
#         if chunk.root.text in ["haircut", "hair dye"] and info[4] not in data:
#             data[info[4]] = chunk.text
#     for token in doc:
#         if token.text in ["gold", "light"] and info[5] not in data:
#             data[info[5]] = token.text
#     return data

# print(extract_appointment_details(text))