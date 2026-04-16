#!/usr/bin/env python3
import os
import streamlit as st
from poi import import_attractions
from models import call_GPT, call_TTS



if __name__ == "__main__":

    st.title("Barcelona Tourist Attractions")
    st.header("Generate text and audio content for Barcelona's top tourist attractions")

    attractions = import_attractions()
    
    attraction_names = [attraction["nice_name"] for attraction in attractions]
    
    selected_attraction = st.radio("Select an attraction:", attraction_names)

    st.write(f"You selected: {selected_attraction}")

    generate = st.button("Generate content")

    if generate:
        model = "gpt-4o-mini"
        prompt = "You are a local travel guide based in Barcelona. Please provide an extensive description of the tourist attraction called " + selected_attraction + ". Include information about its history, architecture, and any interesting facts. Also, describe location, opening hours, the best time to visit and any nearby attractions or food options worth exploring. This content will help you plan your visit but also to guide you through the experience when you are there. Please provide the information in a friendly and engaging tone, as if you were sharing it with a friend who is visiting Barcelona for the first time."
        res = call_GPT(model, prompt)
        call_TTS("gpt-4o-mini-tts",res.content)
        st.audio("attraction.mp3")
        st.write(res.content)
        
    
    