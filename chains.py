#!/usr/bin/env python3
from itertools import chain
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv('.env')

def call_gpt_stream_chain(model : str, user_input : dict, temperature : float | None = None):
    kwargs = {
        "model" : model,
        "api_key" : os.getenv("OPENAI_API_KEY"),
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    
    prompt_tmpl = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that provides information about tourist attractions in Barcelona. Include information about its history, architecture, and any interesting facts. Also, describe location, opening hours, the best time to visit and any nearby attractions and nearby food options worth exploring. This content will help you plan your visit but also to guide you through the experience when you are there. Please provide the information in a friendly and engaging tone, as if you were sharing it with a friend who is visiting Barcelona for the first time, but still keep it with a level of formality. Please end with a wrap-up section and not include any next steps."),
        ("human", "Please provide an extensive description of the tourist attraction called {attraction_name}. ")
        ])
    llm = ChatOpenAI(**kwargs)

    chain = prompt_tmpl | llm

    for chunk in chain.stream({"attraction_name": user_input["attraction_name"]}):
        if chunk.content:
            yield chunk.content


if __name__ == "__main__":
    attraction_name = "Spotify Camp Nou"
    #prompt_template = ChatPromptTemplate.from_messages([
    #    ("system", "You are a helpful assistant that provides information about tourist attractions in Barcelona. Include information about its history, architecture, and any interesting facts. Also, describe location, opening hours, the best time to visit and any nearby attractions and nearby food options worth exploring. This content will help you plan your visit but also to guide you through the experience when you are there. Please provide the information in a friendly and engaging tone, as if you were sharing it with a friend who is visiting Barcelona for the first time."),
    #    ("human", "Please provide an extensive description of the tourist attraction called {attraction_name}. ")
    #    ])
    #model = ChatOpenAI(model_name="gpt-5.2-chat-latest", temperature=0.15)
    #% Chain
    #chain = prompt_template | model | StrOutputParser()
    for text in call_gpt_stream_chain(model="gpt-5.2-chat-latest", user_input={"attraction_name": attraction_name}):
        print(text, end="", flush=True)
    
    print("\n End ...")
