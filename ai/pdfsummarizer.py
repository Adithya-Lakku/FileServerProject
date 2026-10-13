
import requests
import json
from PyPDF2 import PdfReader
import asyncio
import os
from db import services as _services


def summarize(file_id,db):

    filepath = _services.get_file_path(file_id,db)

    text = readPdf(filepath=filepath)
    if(text):
        print(text)

    url = "http://ollama:11434/api/generate" #usually is "http://localhost:11434/api/generate"


    #prompt = f"summarize the text in 300 characters {text}"

    payload = {
    "model": "gemma3:4b",
    "prompt": f"summarize the text in 200 words{text} with proper spacing ",
    #"prompt": "just say hello",
    "stream": False
    }

    response = requests.post(url,json=payload,stream=False)

    data = response.json()
    
    try:

        if response.status_code == 200:
            print("ai success")

            
            # print(data)
            # if "message" in data and "content" in data["message"]:
            #     output = data["message"]["content"]
            #     print("output is:"+output)
            #     print("data is: "+data)
                
            #     return output
            

            if 'response' in data:
                output = data['response']

                _services.updateMetadata(file_id, {"summary": output}, db)
                
                return output


        else:
            print("ai fail")
    except json.JSONDecodeError:
        print("shit failed")        

    




def readPdf(filepath): # read pdf text
    reader = PdfReader(filepath) 


    text = ''

    # Read text from each page
    for page in reader.pages:
        text = text + page.extract_text()

    

    return text

def Summarizerv2(text): #modified version of summarizerv1 to use ollama as llm engine
    
    url = "http://ollama:11434/api/generate" #usually is "http://localhost:11434/api/generate"


    #prompt = f"summarize the text in 300 characters {text}"

    payload = {
    "model": "gemma3:4b",
    "prompt": f"summarize the text in 300 characters {text}",
    "stream": False
}

    response = requests.post(url,json=payload,stream=False)

    data = response.json()
    
    try:

        if response.status_code == 200:
            print("ai success")
            if "message" in data and "content" in data["message"]:
                output = data["message"]["content"]
                print(output)
                return output
        else:
            print("ai fail")
    except json.JSONDecodeError:
        print("shit failed")





# def post_to_discord(text): # post to discord 💀

    
#     response = requests.post(DiscordWebhookUrl,json={"content": text})

#     if response.status_code == 204:
#         print(" discord success")
#     else :
#         print("discord fail")


# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f'✅ Logged in as {client.user}')
#     dummytester()

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     for attachment in message.attachments:
#         print(f"📄 PDF received: {attachment.filename}")

#         #  Download the PDF to your local PC
#         file_path = os.path.join("downloads", attachment.filename)
#         os.makedirs("downloads", exist_ok=True)
#         await attachment.save(file_path)
        
#         text = readPdf(filepath=file_path)
#         text1 = Summarizerv2(text)
        
#         post_to_discord(text1)
        

#         print(f"💾 Saved to {file_path}")
#         break

# client.run(DiscordBotToken)