import pathlib
import textwrap
from openai import AzureOpenAI
import os
import gradio as gr


API_KEY=os.getenv('AZURE_OPENAI_API_KEY')
API_ENDPOINT=os.getenv('AZURE_OPENAI_ENDPOINT')

# This is the first user message that will be sent to the model. Feel free to update this.
user_message = ""
system_message="You are english grammer expert"

# Create the list of messages. role can be either "user" or "assistant" 
messages=[
    {"role": "system", "content":system_message },
    {"role": "user", "name":"example_user", "content":"" }
]

client=AzureOpenAI(
   api_key=API_KEY,
   api_version="2024-02-01",
   azure_endpoint= API_ENDPOINT,
   azure_deployment="Hackathons"   
)


def send_message(messages, max_response_tokens=4096):
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages,    
        temperature=0.5,
        max_tokens=max_response_tokens
    )
    return response.choices[0].message.content

# Defining a function to print out the conversation in a readable format
def print_conversation(messages):
    for message in messages:
        print(f"[{message['role'].upper()}]")
        print(message['content'])
        print()

# Defining a function to print out the conversation in a readable format
def get_conversation(messages):
    for message in messages:
        return message['content']

def azure_chat_builder(language_input,type_input,name_input,details_input):
    messages=[]
    responsebuild=f"Pleae creaate pseudonym which is {type_input} for {name_input} with {details_input} in language {language_input}"
    messages=[
    {"role": "system", "content":system_message }
    ]
    messages.append({"role": "user", "content": responsebuild})
    response = send_message(messages, 4096)
    #responsebuild1=response
    return response

demo=gr.Interface(
    azure_chat_builder,[
    gr.Dropdown(
        ["English","Spanish","Chinese","Japanese","Korean","Hindi"],multiselect=False,label="Language",info="Select Language",value="English"
    ),
    gr.Dropdown(
        ["Gamer","Funny","Author","Clothing","Software"],multiselect=False,label="Type",info="Select Type of Pseudonym",value="Gamer"
    ),
    gr.Textbox(
        label="Input Details",
        info="Add details to create more meaningful Pseudonym",
        lines=1,
        value="Gamer who is fast as light"
    )],
    "text",title="Pseudonym Generator",css="footer {visibility: hidden}",allow_flagging="never",submit_btn=gr.Button("Generate")
)

if __name__=='__main__':
    demo.launch()



