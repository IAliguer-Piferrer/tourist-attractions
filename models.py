#!/usr/bin/env python3
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))
# %%
def call_GPT(model, prompt):
    # %% OpenAI models
    # https://platform.openai.com/docs/models/overview
    model = ChatOpenAI(model_name=model,
                       temperature=0.25, # controls creativity
                       api_key=os.getenv('OPENAI_API_KEY'))
    return model.invoke(prompt)

def call_GPT_stream(model, prompt):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    response = client.chat.completions.create(
                       model=model,
                       temperature=0.3, # controls creativity
                       messages=[{"role": "user", "content": prompt}],
                       stream=True)
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
    

def call_TTS(model, text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.audio.speech.create(model=model, 
                                          input=text, 
                                          voice="fable")
    with open("attraction.mp3", "wb") as f:
        f.write(response.content)
    return

if __name__ == "__main__":
    model = "gpt-4o-mini"
    attraction = "Spotify Camp Nou"
    prompt = "You are a local travel guide based in Barcelona. Please provide an extensive description of the tourist attraction called " + attraction + ". Include information about its history, architecture, and any interesting facts. Also, describe location, opening hours, the best time to visit and any nearby attractions or food options worth exploring. This content will help you plan your visit but also to guide you through the experience when you are there. Please provide the information in a friendly and engaging tone, as if you were sharing it with a friend who is visiting Barcelona for the first time."
    #res = call_GPT(model, prompt)
    #print(res.content)
    #call_TTS("gpt-4o-mini-tts",res.content)
    print("Streaming response:")
    for chunk in call_GPT_stream(model, prompt):
        print(chunk, end="")
    
    print("End...")